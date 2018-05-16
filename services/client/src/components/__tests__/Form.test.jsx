import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';

import Form from '../Form';

const testData = [
    {
        formType: 'Register',
        formData: {
            username: '',
            email: '',
            password: ''
        }
    },
    {
        formType: 'Login',
        formData: {
            email: '',
            password: ''
        }
    }
];

testData.forEach((e1) => {
    test('${e1.formType} Form renders properly', () => {
        const component = <Form formType={e1.formType} formData={e1.formData} />;
        const wrapper = shallow(component);
        const h1 = wrapper.find('h1');
        expect(h1.length).toBe(1);
        expect(h1.get(0).props.children).toBe(e1.formType);
        const formGroup = wrapper.find('.form-group');
        expect(formGroup.length).toBe(Object.keys(e1.formData).length);
        expect(formGroup.get(0).props.children.props.name).toBe(Object.keys(e1.formData)[0]);
        expect(formGroup.get(0).props.children.props.value).toBe('');
    });
    test('${e1.formType} Form renders a snapshot properly', () => {
        const component = <Form formType={e1.formType} formData={e1.formData} />;
        const tree = renderer.create(component).toJSON();
        expect(tree).toMatchSnapshot();
    });
});
