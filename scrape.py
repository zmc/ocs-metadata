#!/usr/bin/env python
import argparse
import jenkins
import json
import logging
import os
import requests

log = logging.getLogger()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--job', '-j', default='ocs-registry-container')
    parser.add_argument('--jenkins-url', '-u', required=True)
    parser.add_argument('--build', '-b', default=None)
    return parser.parse_args()


def main(args=None):
    args = args or parse_args()
    scraper = JenkinsScraper(args.jenkins_url)
    if args.build:
        build_info = scraper.get_build_info(
            args.job,
            int(args.build),
            depth=1
        )
        builds = [build_info]
    else:
        builds = scraper.get_successful_builds(args.job)
    result = list()
    for build in builds:
        image_versions = scraper.get_image_versions(build)
        if image_versions:
            result.append(image_versions)
    print(json.dumps(result))


class JenkinsScraper(jenkins.Jenkins):
    ARTIFACTS = [
        'image_versions.txt', 'image_versions.json', 'ocs_registry_tag.txt']

    def __init__(self, url):
        super().__init__(url)

    def get_successful_builds(self, job_name):
        job_info = self.get_job_info(job_name, depth=1)
        return [build for build in job_info['builds']
                if build['result'].lower() == 'success']

    def get_artifacts(self, build_info):
        content = dict()
        for artifact in build_info['artifacts']:
            if not artifact['fileName'] in self.ARTIFACTS:
                continue
            url = os.path.join(
                build_info['url'],
                'artifact',
                artifact['relativePath']
            )
            req = requests.Request(method='GET', url=url)
            resp = self.jenkins_request(req)
            resp.raise_for_status()
            content[artifact['fileName']] = resp.text
        return content

    def get_image_versions(self, build_info):
        artifacts = self.get_artifacts(build_info)
        result = dict(
            product='OCS',
            url=build_info['url'],
            version=artifacts['ocs_registry_tag.txt'].strip(),
            contents=[],
        )
        if 'image_versions.txt' in artifacts.keys():
            # This code can parse builds that happened before we switched to
            # storing the image versions as JSON, but those buidls lack the
            # separate tag and URI metadata, so we should probably just skip
            # them
            log.warning(
                "Skipping build with old artifact format: %s",
                result['version']
            )
            return None
            image_strs = artifacts['image_versions.txt'].strip().split('\n')
            for image_str in image_strs:
                try:
                    image, version = image_str.split('=')
                except ValueError:
                    # This is likely one of the handful of builds that had a
                    # not-very-machine-readable format, so let's skip.
                    log.warning(
                        "Skipping build with invalid artifacts: %s",
                        result['version']
                    )
                    return None
                result['contents'].append(dict(name=image, version=version))
        elif 'image_versions.json' in artifacts.keys():
            contents = json.loads(artifacts['image_versions.json'])
            if isinstance(contents, dict):
                result['contents'] = [
                    dict(list(value.items()) + [('name', key)])
                    for key, value in contents.items()
                ]
            else:
                result['contents'] = contents
        else:
            raise RuntimeError("No image_versions! %s" % build_info)
        return result


if __name__ == '__main__':
    main()
