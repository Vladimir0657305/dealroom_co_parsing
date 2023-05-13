const puppeteer = require('puppeteer');
const url = 'https://app.dealroom.co/lists/33805?sort=-startup_ranking_rating';
const lastPage = 2;

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    await page.goto(url, { waitUntil: 'networkidle2' });

    const firmsData = [];
    let counter = 1;

    for (let i = 1; i <= lastPage; i++) {
        const links = await page.$$eval('a.entity-name__name-text', (els) => els.map((el) => el.href));
        const allDealroomLinks = links.map((link) => new URL(link, url).href);

        for (let j = 0; j < allDealroomLinks.length; j++) {
            const dealroomLink = allDealroomLinks[j];
            await page.goto(dealroomLink, { waitUntil: 'networkidle2' });

            const name = await page.$eval('h1.name', (el) => el.textContent.trim() || 'No name data');
            const description = await page.$eval(
                'div.item-details-info__details div.tagline',
                (el) => el.textContent.trim() || 'No description data'
            );
            const website = await page.$eval(
                'div.entity-details div.details div.item-details-info__website a[href]',
                (el) => el.textContent.trim() || 'No website data'
            );
            const linkedin = await page.$eval('div.resource-urls', (el) => {
                const spanElement = el.querySelector('a[href*=linkedin]');
                if (spanElement) {
                    return spanElement.href || 'No LinkedIn data';
                }
                return 'No LinkedIn data';
            });

            firmsData.push({ Name: name, Description: description, Website: website, LinkedIn: linkedin });
            console.log(`Processed ${counter} firm(s).`);
            counter++;
        }

        if (i < lastPage) {
            await Promise.all([
                page.click('.pagination-next'),
                page.waitForNavigation({ waitUntil: 'networkidle2' }),
            ]);
        }
    }

    await browser.close();

    console.log('Done');
})();
