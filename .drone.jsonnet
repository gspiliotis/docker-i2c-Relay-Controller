local base_img = 'python:alpine';
local repo = 'angelnu/i2c-relay';
local archs = [
  "amd64",
  "arm",
  "arm64"
];

local Build_Docker_Step(arch, prefix) = {
  name: prefix + 'docker',
  image: 'plugins/docker',
  settings: {
    repo: repo,
    tags: [
      prefix + "${DRONE_BRANCH}-${DRONE_BUILD_NUMBER}-${DRONE_COMMIT}-"+arch,
      prefix + "${DRONE_BRANCH}-"+arch,
      prefix + "latest-"+arch,
    ],
    cache_from: [
      #docker cache
      repo + ":" + prefix + "master-"+arch,
      repo + ":" + prefix + "${DRONE_BRANCH}-"+arch,

      #previous build step
      repo + ":" + "${DRONE_BRANCH}-"+arch,

      #Base repo
      base_img
    ],
    #target: prefix + "iobroker",
    username: {
      from_secret: 'DOCKER_USER'
    },
    password: {
      from_secret: 'DOCKER_PASS'
    },
    build_args: [
      'BASE='+base_img,
      'arch='+arch,
    ],
  }
};

local Build_Pipeline(arch) = {
  kind: 'pipeline',
  name: 'build_'+arch,
  platform: {
    os: 'linux',
    arch: arch,
  },
  steps: [
    Build_Docker_Step(arch, ""),
  ],
};

local Manifest_Step(platforms, prefix, tag) = {
  "name": "manifest_" + prefix + tag,
  "image": "plugins/manifest:1",
  "group": "manifest",
  "settings": {
    "username": {
      "from_secret": "DOCKER_USER"
    },
    "password": {
      "from_secret": "DOCKER_PASS"
    },
    "target": repo+":" + prefix + tag,
    "ignore_missing": true,
    "template": repo + ":" + prefix + "${DRONE_BRANCH}-${DRONE_BUILD_NUMBER}-${DRONE_COMMIT}-ARCH",
    "platforms": ["linux/"+platform for platform in platforms]
  }
};

local Manifest_Pipeline(platforms) = {
  "kind": "pipeline",
  "name": "build_manifest",
  depends_on: ["build_"+platform for platform in platforms],
  "steps": [
    Manifest_Step(platforms,"", "${DRONE_BRANCH}-${DRONE_BUILD_NUMBER}-${DRONE_COMMIT}"),
    Manifest_Step(platforms,"", "${DRONE_BRANCH}"),
    Manifest_Step(platforms,"", "latest"),
  ]
};



[ Build_Pipeline(arch) for arch in archs
]+[
  Manifest_Pipeline(archs)
]
