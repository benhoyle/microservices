import { Selector } from 'testcafe';

const TEST_URL = process.env.TEST_URL;

fixture('/').page(`${TEST_URL}/`);

test(`users should be able to view the '/' page`, async (t) => {
    await t
        .navigateTo(TEST_URL)
        .expect(Selector('H1').withText('All Users').exists).ok()
});

test(`users should see the login form on the '/login' page`, async (t) => {
    await t
        .navigateTo('login')
        .expect(Selector('H1').withText('Login').exists).ok()
});
