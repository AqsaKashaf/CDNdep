/* 
sudo apt-get -y install libnss3 libxss1 libasound2 libatk-bridge2.0-0 libgtk-3-0 libgbm-dev
cd ~
curl -sL https://deb.nodesource.com/setup_16.x -o /tmp/nodesource_setup.sh
sudo bash /tmp/nodesource_setup.sh
sudo apt install -y nodejs
npm install puppeteer
npm install puppeteer-har
*/

const puppeteer = require('puppeteer');
const PuppeteerHar = require('puppeteer-har');
const fs = require('fs');

website = process.argv[2]
dir = process.argv[3]

get_har(website)
async function get_har(website) {

  if (!fs.existsSync(dir)){
      fs.mkdirSync(dir);
  }
  let result_filename = "harfiles/" + website + '.har';
  if(fs.existsSync(result_filename)){
    return
  }
  if (!fs.existsSync(result_filename)) {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    const har = new PuppeteerHar(page);
    await har.start({ path: result_filename});
    try {
      await page.goto(`http://${website}`,{
        waitUntil: 'domcontentloaded',
        timeout: 0,
       });
    } catch (e) {
      fs.appendFileSync("harfiles/harlogs", website + ",error" + e.toString() + "\n");
      return -1
    }
    await har.stop();
    await browser.close();
  }
  return 0
}


