import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';

import Form from '../Form';

const testData = [
    {
        formType: 'register',
        formData: {
            username: '',
            email: '',
            password: ''
        },
        loginUser: jest.fn(),
        isAuthenticated: false,
    },
    {
        formType: 'login',
        formData: {
            email: '',
            password: ''
        },
        loginUser: jest.fn(),
        isAuthenticated: false,
    }
];

describe('When not authenticated', () => {
    testData.forEach((e1) => {
        const component = <Form {...e1} />;
        it('${e1.formType} Form renders properly', () => {
            const wrapper = shallow(component);
            const h1 = wrapper.find('h1');
            expect(h1.length).toBe(1);
            expect(h1.get(0).props.children).toBe(e1.formType);
            const formGroup = wrapper.find('.form-group');
            expect(formGroup.length).toBe(Object.keys(e1.formData).length);
            expect(formGroup.get(0).props.children.props.name).toBe(Object.keys(e1.formData)[0]);
            expect(formGroup.get(0).props.children.props.value).toBe('');
        });
        it(`${e1.formType} Form submits the form properly`, () => {
            const wrapper = shallow(component);
            wrapper.instance().handleUserFormSubmit = jest.fn();
            wrapper.update();
            const input = wrapper.find('input[type="email"]');
            expect(wrapper.instance().handleUserFormSubmit).toHaveBeenCalledTimes(0);
            input.simulate(
                'change', { target: { name: 'email', value: 'test@test.com' } }
                )
            wrapper.find('form').simulate('submit', e1.formData)
            expect(wrapper.instance().handleUserFormSubmit).toHaveBeenCalledWith(
                e1.formData);
            expect(wrapper.instance().handleUserFormSubmit).toHaveBeenCalledTimes(1);
        });
        it('${e1.formType} Form renders a snapshot properly', () => {
            const tree = renderer.create(component).toJSON();
            expect(tree).toMatchSnapshot();
        });
    })
});


describe('When authenticated', () => {
    testData.forEach((e1) => {
        const component = <Form
            formType={e1.formType}
            formData={e1.formData}
            isAuthenticated={true}
        />;
        it('${e1.formType} redirects properly', () => {
            const wrapper = shallow(component);
            expect(wrapper.find('Redirect')).toHaveLength(1);
        });
    });
});
