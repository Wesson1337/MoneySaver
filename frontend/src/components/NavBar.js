import React, {useState} from 'react';
import {Button, Container, Nav, Navbar} from "react-bootstrap";
import dollar from "../static/dollar-white.svg"
import {useNavigate} from "react-router-dom";
import {ACCOUNTS_ROUTE, LOGIN_ROUTE, MAIN_PAGE_ROUTE, OPERATIONS_ROUTE} from "../utils/consts";
import {useAuth} from "../context/Auth";
import {logout} from "../http/userAPI";

const NavBar = () => {
    const navigate = useNavigate()
    const [active, setActive] = useState("")
    const {user, setUser} = useAuth()
    return (
            <>
      <Navbar bg="dark" variant="dark" expand="lg">
        <Container>
            <Navbar.Brand onClick={() => {setActive(""); navigate(MAIN_PAGE_ROUTE)}} style={{cursor: "pointer"}}>
                <img
                  alt=""
                  src={dollar}
                  width="30"
                  height="30"
                  className="d-inline-block align-top"
                />{' '}
                MoneySaver
            </Navbar.Brand>
            <Navbar.Toggle aria-controls="navbarScroll" />
            <Navbar.Collapse id="navbarScroll">
                <Nav
                    className="me-auto my-2 my-lg-0"
                    activeKey={active}
                    onSelect={(selectedKey) => {user ? setActive(selectedKey) : setActive("")}}
                    navbarScroll
                    style={{maxWidth: "100px"}}
                >
                <Nav.Link eventKey="accounts" onClick={() => navigate(ACCOUNTS_ROUTE)}>Accounts</Nav.Link>
                <Nav.Link eventKey="operations" onClick={() => navigate(OPERATIONS_ROUTE)}>Operations</Nav.Link>
                </Nav>
                {user
                    ?
                    <Button onClick={() => {logout(); setUser(""); setActive(""); navigate(LOGIN_ROUTE)}} variant="outline-secondary">
                        Sign out
                    </Button>
                    :
                    <Button onClick={() => {setActive(""); navigate(LOGIN_ROUTE)}} variant="outline-secondary">
                        Sign in
                    </Button>
                }
            </Navbar.Collapse>
        </Container>
      </Navbar>
    </>
    );
};

export default NavBar;