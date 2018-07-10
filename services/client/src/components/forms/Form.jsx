import React, { Component } from 'react';
import axios from 'axios';
import { Redirect } from 'react-router-dom';
import { registerFormRules, loginFormRules } from './form-rules.js';
import FormErrors from './FormErrors.jsx';

class Form extends Component {
    constructor(props) {
        super(props);
        this.state = {
            formData: {
                username: '',
                email: '',
                password: ''
            },
            registerFormRules: registerFormRules,
            loginFormRules: loginFormRules,
            valid: false,
        };
        this.handleUserFormSubmit = this.handleUserFormSubmit.bind(this);
        this.handleFormChange = this.handleFormChange.bind(this);
    };
    componentDidMount() {
        this.clearForm();
    };
    componentWillReceiveProps(nextProps) {
        if (this.props.formType !== nextProps.formType) {
            this.clearForm();
        };
    };
    clearForm() {
        this.setState({
            formData: {
                username: '',
                email: '',
                password: ''
            }
        });
    };
    handleFormChange(event) {
        const obj = this.state.formData;
        obj[event.target.name] = event.target.value;
        this.setState(obj);
        this.validateForm();
    };
    handleUserFormSubmit(event) {
        event.preventDefault();
        // Get form type from URL
        const formType = this.props.formType;
        let data;
        if (formType === 'login') {
            data = {
                email: this.state.formData.email,
                password: this.state.formData.password
            }
        };
        if (formType === 'register') {
            data = {
                username: this.state.formData.username,
                email: this.state.formData.email,
                password: this.state.formData.password
            }
        };
        const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/auth/${formType}`
        axios.post(url, data)
        .then((res) => {
            this.clearForm();
            this.props.loginUser(res.data.auth_token);
        })
        .catch((err) => { console.log(err); });
    };
    validateForm() {
        // define self as this
        const self = this;
        // get form data
        const formData = this.state.formData;
        // reset all rules
        self.resetRules()
        // validate register form
        if (self.props.formType === 'register') {
            const formRules = self.state.registerFormRules;
            if (formData.password.length > 10) formRules[3].valid = true;
            self.setState({registerFormRules: formRules});
            if (self.allTrue()) self.setState({valid: true});
        };
        this.setState({ valid: true });
    };
    allTrue() {
        let formRules = this.state.loginFormRules;
        if (this.props.formType === 'register') {
            formRules = this.state.registerFormRules;
        };
        for (const rule of formRules) {
            if (!rule.valid) return false;
        };
        return true;
    };
    resetRules() {
        if (this.props.formType === 'login') {
            const formRules = this.state.loginFormRules;
            for (const rule of formRules) {
                rule.valid = false;
            };
            this.setState({loginFormRules: formRules});
        };
        if (this.props.formType === 'register') {
            const formRules = this.state.registerFormRules;
            for (const rule of formRules) {
                rule.valid = false;
            };
            this.setState({registerFormRules: formRules});
        };
        this.setState({valid: false});
    };
    render () {
        if (this.props.isAuthenticated) {
            return <Redirect to='/' />;
        };
        let formRules = this.state.loginFormRules;
        if (this.props.formType === 'register') {
            formRules = this.state.registerFormRules;
        };
        return (
            <div>
                <h1 style={{'textTransform':'capitalize'}}>{this.props.formType}</h1>
                <hr/><br/>
                <FormErrors
                    formType={this.props.formType}
                    formRules={formRules}
                />
                <form onSubmit={(event) => this.handleUserFormSubmit(event)}>
                    {this.props.formType === 'register' &&
                        <div className="form-group">
                            <input
                                name="username"
                                className="form-control input-lg"
                                type="text"
                                placeholder="Enter a username"
                                required
                                value={this.state.formData.username}
                                onChange={this.handleFormChange}
                            />
                        </div>
                    }
                    <div className="form-group">
                        <input
                            name="email"
                            className="form-control input-lg"
                            type="email"
                            placeholder="Enter an email address"
                            required
                            value={this.state.formData.email}
                            onChange={this.handleFormChange}
                        />
                    </div>
                    <div className="form-group">
                        <input
                            name="password"
                            className="form-control input-lg"
                            type="password"
                            placeholder="Enter a password"
                            required
                            value={this.state.formData.password}
                            onChange={this.handleFormChange}
                        />
                    </div>
                    <input
                        type="submit"
                        className="btn btn-primary btn-lg btn-block"
                        value="Submit"
                        disabled={!this.state.valid}
                    />
                </form>
            </div>
        )
    };
};

export default Form;
