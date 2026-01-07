module.exports = {
  project: 'VERTIV_V6_GLOBAL',
  apps: [
    {
      name: 'backend',
      path: './apps/backend',
      type: 'cloud-run',
      region: 'us-central1'
    },
    {
      name: 'frontend',
      path: './apps/frontend',
      type: 'cloud-run',
      region: 'us-central1'
    }
  ]
};
