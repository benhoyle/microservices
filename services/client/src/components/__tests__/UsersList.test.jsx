import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';

import UsersList from '../UsersList';

const users = [
    {
        'active': true,
        'email': 'ben@gmail.com',
        'id' : 1,
        'username': 'ben'
    },
    {
        'active': true ,
        'email': 'jimbob@email.co.uk' ,
        'id': 2 ,
        'username': 'jimbob'
    }
];

test('UsersList renders properly', () => {
    const wrapper = shallow(<UsersList users={users}/>);
    const element = wrapper.find('h4');
    expect(element.length).toBe(2);
    expect(element.get(0).props.className).toContain('well');
    expect(element.get(0).props.children).toBe('ben');
});

test('UsersList renders a snapshot properly', () => {
    const tree = renderer.create(<UsersList users={users}/>).toJSON();
    expect(tree).toMatchSnapshot();
});
