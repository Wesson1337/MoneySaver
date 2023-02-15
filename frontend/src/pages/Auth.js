import React, {useState} from 'react';
import {useAuth} from "../context/Auth";
import {NavLink, useLocation, useNavigate} from "react-router-dom";
import {LOGIN_ROUTE, MAIN_PAGE_ROUTE, REGISTRATION_ROUTE} from "../utils/consts";
import {login} from "../http/userAPI";
import {Button, Card, Container, Form, Nav, Row} from "react-bootstrap";

const Auth = () => {
    const location = useLocation()
    const isLogin = location.pathname === LOGIN_ROUTE
    const {email, setEmail} = useState('')
    const {password1, setPassword1} = useState('')
    const {password2, setPassword2} = useState('')
    const {user, setUser} = useAuth()
    const navigate = useNavigate()

    const loginClick = async () => {
        const response = await login(email, password1)
        console.log(response)
    }

    const goToMain = () => {
        navigate(MAIN_PAGE_ROUTE)
    }

    const goToRegistration = () => {

    }


    return (
        <Container
            className="d-flex justify-content-center align-items-center"
            style={{height: window.innerHeight}}
        >
            <Card style={{width: 600}} className="p-5">
                <h2 className="m-auto">{isLogin ? 'Login' : 'Sign up'}</h2>
                <Form classname="d-flex flex-column">
                    <Form.Control
                        className="mt-3"
                        placeholder="Insert your email..."
                        type="email"
                    >
                    </Form.Control>
                    <Form.Control
                        className="mt-3"
                        placeholder="Insert your password..."
                        type="password"
                    >
                    </Form.Control>
                    {isLogin ?
                        '' :
                        <Form.Control
                        className="mt-3"
                        placeholder="Repeat your password..."
                        type="password"
                        >
                        </Form.Control>
                    }
                    <Row className="d-flex justify-content-between mt-3 pl-3 pr-3 gap-3">
                        {isLogin ?
                            <div className="w-auto">
                                Don't have an account? <NavLink to={REGISTRATION_ROUTE}>Sign up!</NavLink>
                            </div>
                            :
                            <div className="w-auto">
                                Have an account? <NavLink to={LOGIN_ROUTE}>Log in!</NavLink>
                            </div>
                        }
                        <Button
                            className="w-auto"
                            style={{marginRight: 11}}
                            variant={"outline-success"}
                        >
                            {isLogin ? 'Log in' : 'Sign up'}
                        </Button>
                    </Row>
                </Form>
            </Card>
        </Container>
    );
};

export default Auth;