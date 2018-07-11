import { Selector } from 'testcafe';

const randomstring = require('randomstring');

const username = randomstring.generate();
const email = `${username}@test.com`;

const TEST_URL = process.env.TEST_URL;
const password = 'greaterthanten';

fixture('/login').page(`${TEST_URL}/login`);

test(`should display the login form`, async (t) => {
    await t
        .navigateTo(`${TEST_URL}/login`)
        .expect(Selector('H1').withText('Login').exists).ok()
        .expect(Selector('form').exists).ok()
        .expect(Selector('input[disabled]').exists).ok()
        .expect(Selector('.validation-list').exists).ok()
        .expect(Selector('.validation-list > .error').nth(0).withText(
            'Email is required.').exists).ok()
});

test(`should allow a user to sign in`, async (t) => {

    // register user
    await t
        .navigateTo(`${TEST_URL}/register`)
        .typeText('input[name="username"]', username)
        .typeText('input[name="email"]', email)
        .typeText('input[name="password"]', password)
        .click(Selector('input[type="submit"]'))

    // log a user out
    await t
        .click(Selector('a').withText('Logout'))

    // log a user in
    await t
        .navigateTo(`${TEST_URL}/login`)
        .typeText('input[name="email"]', email)
        .typeText('input[name="password"]', password)
        .click(Selector('input[type="submit"]'))

    // assert user is redirected to '/'
    // assert '/' is displayed properly
    const tableRow = Selector('td').withText(username).parent();
    await t
        .expect(Selector('H1').withText('All Users').exists).ok()
        .expect(tableRow.child().withText(username).exists).ok()
        .expect(tableRow.child().withText(email).exists).ok()
        .expect(Selector('a').withText('Status').exists).ok()
        .expect(Selector('a').withText('Logout').exists).ok()
        .expect(Selector('a').withText('Register').exists).notOk()
        .expect(Selector('a').withText('Login').exists).notOk()


    // log a user out
    await t
        .click(Selector('a').withText('Logout'))

    // assert '/logout' is displayed properly
    await t
        .expect(Selector('p').withText('You are now logged out').exists).ok()
        .expect(Selector('a').withText('Status').exists).notOk()
        .expect(Selector('a').withText('Logout').exists).notOk()
        .expect(Selector('a').withText('Register').exists).ok()
        .expect(Selector('a').withText('Login').exists).ok()

});

test(`should throw an error if the credentials are incorrect`, async (t) => {

    // attempt to login
    await t
        .navigateTo(`${TEST_URL}/login`)
        .typeText('input[name="email"]', 'incorrect@email.com')
        .typeText('input[name="password"]', password)
        .click(Selector('input[type="submit"]'))

    // assert user login fails
    await t
        .expect(Selector('H1').withText('Login').exists).ok()
        .expect(Selector('a').withText('Status').exists).notOk()
        .expect(Selector('a').withText('Logout').exists).notOk()
        .expect(Selector('a').withText('Register').exists).ok()
        .expect(Selector('a').withText('Login').exists).ok()
        .expect(Selector('.alert-success').exists).notOk()
        .expect(Selector('.alert-danger').withText(
            'Login failed.').exists).ok()

    // attempt to login
    await t
        .navigateTo(`${TEST_URL}/login`)
        .typeText('input[name="email"]', email)
        .typeText('input[name="password"]', 'incorrectpassword')
        .click(Selector('input[type="submit"]'))

    // assert user login fails
    await t
        .expect(Selector('H1').withText('Login').exists).ok()
        .expect(Selector('a').withText('Status').exists).notOk()
        .expect(Selector('a').withText('Logout').exists).notOk()
        .expect(Selector('a').withText('Register').exists).ok()
        .expect(Selector('a').withText('Login').exists).ok()
        .expect(Selector('.alert-success').exists).notOk()
        .expect(Selector('.alert-danger').withText(
            'Login failed.').exists).ok()
});
