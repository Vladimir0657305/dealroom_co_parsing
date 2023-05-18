const puppeteer = require('puppeteer');
const url = 'https://app.dealroom.co/lists/33805?sort=-startup_ranking_rating';
const lastPage = 2;

(async () => {
    const browser = await puppeteer.launch({ executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', headless: "new" });

    const page = await browser.newPage();

    await page.goto(url, { waitUntil: 'networkidle2', timeout: 5000 });

    await page.evaluate(async () => {
        await new Promise((resolve) => {
            let totalHeight = 0;
            let distance = 100;
            let timer = setInterval(() => {
                let scrollHeight = document.body.scrollHeight;
                window.scrollBy(0, distance);
                totalHeight += distance;

                if (totalHeight >= scrollHeight) {
                    clearInterval(timer);
                    resolve();
                }
            }, 500);
        });
    });


    const firmsData = [];
    let counter = 1;

    for (let i = 1; i <= lastPage; i++) {
        const links = await page.$$eval('a.entity-name__name-text', (els) => els.map((el) => el.href));
        const allDealroomLinks = links.map((link) => new URL(link, url).href);

        for (let j = 0; j < allDealroomLinks.length; j++) {
            const dealroomLink = allDealroomLinks[j];
            console.log(dealroomLink);
            await page.goto(dealroomLink, { waitUntil: 'networkidle2' });

            const name = await page.$eval('h1.name', (el) => el.textContent.trim() || 'No name data');
            // console.log(name);
            const descriptionText = await page.$('div.item-details-info__details div.tagline');
            const description = descriptionText ? await page.evaluate(el => el.textContent.trim(), descriptionText) : 'No description data';
            // console.log(description);
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
            // console.log(linkedin);

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
    
    // Запись в csv файл =======================================================================================
    const createCsvWriter = require('csv-writer').createArrayCsvWriter;
    const csvWriter = createCsvWriter({
        header: ['Name', 'Description', 'Website', 'LinkedIn'],
        path: 'firmsData.csv'
    });
    await csvWriter.writeRecords(firmsData);

    // Запись в xlsx файл =======================================================================================
    const ExcelJS = require('exceljs');

    const workbook = new ExcelJS.Workbook();
    const worksheet = workbook.addWorksheet('My Worksheet');

    // добавление заголовков
    worksheet.columns = [
        { header: 'Name', key: 'name', width: 20 },
        { header: 'Description', key: 'description', width: 50 },
        { header: 'Website', key: 'website', width: 30 },
        { header: 'LinkedIn', key: 'linkedin', width: 30 },
    ];

    // добавление данных
    const firmsDataSave = [
        { Name: 'Firm 1', Description: 'Description 1', Website: 'www.firm1.com', LinkedIn: 'www.linkedin.com/firm1' },
        { Name: 'Firm 2', Description: 'Description 2', Website: 'www.firm2.com', LinkedIn: 'www.linkedin.com/firm2' },
    ];

    firmsDataSave.forEach((data) => {
        worksheet.addRow(data);
    });

    // сохранение в файл
    workbook.xlsx.writeFile('output.xlsx')
        .then(() => {
            console.log('File saved!');
        });

    console.log('Done');
})();
