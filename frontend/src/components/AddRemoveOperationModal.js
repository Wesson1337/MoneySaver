import React, {useEffect, useState} from 'react';
import {Col, Form, Modal, Row} from "react-bootstrap";
import {ACCOUNT_TYPES, CURRENCIES_AND_SYMBOLS, INCOME_CATEGORIES, SPENDING_CATEGORIES} from "../utils/consts";
import Select from "react-select";
import {prettifyFloat} from "../utils/prettifyFloat";
import {convertCurrency} from "../utils/currency";

const AddRemoveOperationModal = ({show, setShow, type, data}) => {
    const isRemove = type === "remove"
    const [categories, setCategories] = useState(null)
    const [currencies, setCurrencies] = useState(null)
    const [accounts, setAccounts] = useState(null)

    useEffect(() => {
        let tempAccounts = []
        data.accounts.forEach((account) => {
            let newAccount = {}
            newAccount["label"] =
                <div className="d-flex justify-content-between">
                    <p className="m-0">{`${account["name"] ? account["name"] : 'Unnamed account'} (${ACCOUNT_TYPES[account["type"]].name})`}</p>
                    <p className="m-0">{`${prettifyFloat(account["balance"])} ${CURRENCIES_AND_SYMBOLS[account["currency"]]}`}</p>
                </div>
            newAccount["value"] = account
            tempAccounts.push(newAccount)
        })
        setAccounts(tempAccounts)
    }, [])

    useEffect(() => {
        let tempCurrencies = []
        Object.entries(CURRENCIES_AND_SYMBOLS).forEach(([key, value]) => {
            let newCurrency = {label: value, value: key}
            tempCurrencies.push(newCurrency)
        })
        setCurrencies(tempCurrencies)
    }, [])

    useEffect(() => {
        let tempCategories = []
        Object.entries(isRemove ? SPENDING_CATEGORIES : INCOME_CATEGORIES).forEach(([key, category]) => {
            let newCategory = {}
            newCategory["label"] = <div
                className="d-flex align-items-center gap-2">
                <img src={category.icon} alt="" height="25px"/>
                <p className="m-0"
                   style={{textAlign: "left"}}>{category.name}</p>
            </div>
            newCategory["value"] = key
            tempCategories.push(newCategory)
        })
        setCategories(tempCategories)
    }, [])

    const [chosenCurrency, setChosenCurrency] = useState(null)
    const [chosenCategory, setChosenCategory] = useState(null)
    const [chosenAccount, setChosenAccount] = useState(null)
    const [enteredAmount, setEnteredAmount] = useState(null)
    const [amountInAccountCurrency, setAmountInAccountCurrency] = useState(null)

    const evalTotalAmountInAccountCurrency = async () => {
        let convertedCurrency
        if (enteredAmount && chosenAccount && chosenCurrency) {
            console.log(enteredAmount, chosenCurrency, chosenAccount)
            convertedCurrency = await convertCurrency(enteredAmount, chosenCurrency, chosenAccount["currency"])
            return prettifyFloat(Number(convertedCurrency).toFixed(2))
        }
    }
    useEffect(() => {
        evalTotalAmountInAccountCurrency().then((value) => {setAmountInAccountCurrency(value)})
    }, [chosenAccount, chosenCurrency, enteredAmount])

    return (<>
        <Modal
            size="lg"
            show={show}
            onHide={() => {
                setChosenCategory(null)
                setShow(false)
            }}
            backdrop="static"
            keyboard={false}
        >
            <Modal.Header closeButton>
                <Modal.Title>New {isRemove ? "spending" : "income"}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form className="d-flex flex-column gap-3">
                    <Row>
                        <Form.Group as={Col}>
                            <Form.Label className="little-text mb-1">Category</Form.Label>
                            <Select
                                placeholder="Select category..."
                                onChange={(v) => {
                                    setChosenCategory(isRemove ? SPENDING_CATEGORIES[v["value"]] : INCOME_CATEGORIES[v["value"]])
                                }}
                                options={categories}
                                styles={{
                                    control: (baseStyles, state) => ({
                                        ...baseStyles,
                                        minWidth: "200px"
                                    }),
                                }}
                            />
                        </Form.Group>
                        <Form.Group as={Col}>
                            <Form.Label className="little-text mb-1">Amount</Form.Label>
                            <div className="d-flex">
                                <Form.Control
                                    value={enteredAmount ? enteredAmount : null}
                                    onChange={(e) => {
                                        setEnteredAmount(e.target.value)
                                    }}
                                    type="number"
                                    style={{minWidth: "150px"}}
                                />
                                <Select
                                    placeholder=""
                                    styles={{
                                        control: (baseStyles, state) => ({
                                            ...baseStyles,
                                            minWidth: "90px"
                                        }),
                                    }}
                                    options={currencies}
                                    onChange={(v) => {setChosenCurrency(v["value"])}}
                                />
                            </div>
                        </Form.Group>
                    </Row>
                    <Row>
                        <Form.Group as={Col}>
                            <Form.Label className="little-text mb-1">Account</Form.Label>
                            <Select
                                placeholder="Select account..."
                                styles={{
                                    control: (baseStyles, state) => ({
                                        ...baseStyles,
                                        minWidth: "90px"
                                    }),
                                }}
                                options={accounts}
                                onChange={(v) => setChosenAccount(v["value"])}
                            />
                        </Form.Group>
                        <Col className="d-flex align-items-end">
                            <p className="m-0 mb-1 fs-4">Total: {amountInAccountCurrency} {chosenAccount ? CURRENCIES_AND_SYMBOLS[chosenAccount["currency"]] : null}</p>
                        </Col>
                    </Row>
                </Form>
            </Modal.Body>
        </Modal>
    </>);
};

export default AddRemoveOperationModal;