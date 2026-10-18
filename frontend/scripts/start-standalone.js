const fs = require('node:fs');
const path = require('node:path');

const frontendDir = path.resolve(__dirname, '..');
const standaloneDir = path.join(frontendDir, '.next', 'standalone');

for (const directory of ['static', 'public']) {
  const source = path.join(frontendDir, directory === 'static' ? '.next' : '', directory);
  if (fs.existsSync(source)) {
    const target = path.join(standaloneDir, directory === 'static' ? '.next' : '', directory);
    fs.cpSync(source, target, { recursive: true });
  }
}

process.chdir(standaloneDir);
process.env.PORT ||= '3000';
process.env.HOSTNAME ||= '0.0.0.0';
require(path.join(standaloneDir, 'server.js'));
