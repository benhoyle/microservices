import { Selector } from 'testcafe';

const TEST_URL = process.env.TEST_URL;

fixture('/').page(`${TEST_URL}/`);

test(`should display the page correctly if a user is not logged in`, async (t) => {
    await t
        .navigateTo(TEST_URL)
        .expect(Selector('H1').withText('All Users').exists).ok()
        .expect(Selector('a').withText('Status').exists).notOk()
        .expect(Selector('a').withText('Logout').exists).notOk()
        .expect(Selector('a').withText('Register').exists).ok()
        .expect(Selector('a').withText('Login').exists).ok()
});

test(`users should see the login form on the '/login' page`, async (t) => {
    await t
        .navigateTo('login')
        .expect(Selector('H1').withText('Login').exists).ok()
});
