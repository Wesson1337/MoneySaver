import React, {useEffect, useState} from 'react';
import {Button, Col, Form, Modal, Row, Spinner} from "react-bootstrap";
import {
    ACCOUNT_TYPES,
    CURRENCIES_AND_SYMBOLS,
    INCOME_CATEGORIES,
    INTERFACE_COLORS,
    SPENDING_CATEGORIES
} from "../../utils/consts";
import Select from "react-select";
import {prettifyFloat} from "../../utils/prettifyFloat";
import {convertCurrency} from "../../utils/currency";
import {getUserIdFromJWT} from "../../http/userAPI";
import {createTransaction} from "../../http/transactionsAPI";
import {handleAmountOnChange} from "../../utils/forms"

const AddTransactionModal = ({show, setShow, type, data, hasChanged, setHasChanged}) => {
    const isRemove = type === "remove"
    const [categories, setCategories] = useState(null)
    const [currencies, setCurrencies] = useState(null)
    const [accounts, setAccounts] = useState(null)
    const [isLoading, setIsLoading] = useState(false)

    useEffect(() => {
        let tempAccounts = []
        data.accounts.forEach((account) => {
            if (account.is_active) {
                let newAccount = {}
                newAccount["label"] =
                    <div className="d-flex justify-content-between">
                        <div className="d-flex gap-2 align-items-center">
                            <img
                                src={ACCOUNT_TYPES[account.type].icon}
                                width={25}
                                alt=""
                            />
                            <p className="m-0">{`${account["name"] ? `${account["name"].substring(0, 12)}${account.name.length > 12 ? "..." : ""}` : 'Unnamed account'}`}</p>
                        </div>
                        <p className="m-0">{`${prettifyFloat(account["balance"])} ${CURRENCIES_AND_SYMBOLS[account["currency"]]}`}</p>
                    </div>
                newAccount["value"] = account
                tempAccounts.push(newAccount)
            }
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
    const [enteredAmountError, setEnteredAmountError] = useState(null)
    const [enteredComment, setEnteredComment] = useState(null)
    const [amountInAccountCurrency, setAmountInAccountCurrency] = useState(null)
    const [amountInAccountCurrencyIsLoading, setAmountInAccountCurrencyIsLoading] = useState(false)
    const [error, setError] = useState("")

    const evalTotalAmountInAccountCurrency = async () => {
        let convertedCurrency
        if (enteredAmount && chosenAccount && chosenCurrency) {
            setAmountInAccountCurrencyIsLoading(true)
            convertedCurrency = await convertCurrency(enteredAmount, chosenCurrency, chosenAccount["currency"])
            return Number(convertedCurrency).toFixed(2)
        }
    }
    useEffect(() => {
        evalTotalAmountInAccountCurrency().then((value) => {
            setAmountInAccountCurrency(value)
        }).finally(() => setAmountInAccountCurrencyIsLoading(false))
    }, [chosenAccount, chosenCurrency, enteredAmount])


    const handleOnHide = () => {
        setChosenCategory(null);
        setChosenAccount(null);
        setEnteredAmount(null);
        setChosenCurrency(null);
        setAmountInAccountCurrency(null)
        setEnteredAmountError(null)
        setShow(false)
        setError("")
    }

    const handleSave = async () => {
        setIsLoading(true)

        if (!chosenAccount || !chosenCategory || !enteredAmount || !chosenCurrency) {
            setError("At least one field is not filled")
            return
        }
        if (isRemove && amountInAccountCurrency > chosenAccount["balance"]) {
            setError("After this spending account balance will go negative")
            return
        }

        const operationData = {
            "user_id": getUserIdFromJWT(),
            "currency": chosenCurrency,
            "category": chosenCategory.nameForRequest,
            "amount": enteredAmount,
            "comment": enteredComment
        }

        if (isRemove) {
            operationData["receipt_account_id"] = chosenAccount.id
        } else {
            operationData["replenishment_account_id"] = chosenAccount.id
        }
        try {
            return await createTransaction(operationData)
        } catch (e) {
            setError(`${e.response?.data.detail || e.response?.data["msg"] || e}`)
        }
    }

    return (<>
        <Modal
            size="lg"
            show={show}
            onHide={handleOnHide}
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
                                    setError("")
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
                                <div className="d-flex flex-column w-100">
                                    <Form.Control
                                        value={enteredAmount ? enteredAmount : ''}
                                        onChange={(e) => {
                                            handleAmountOnChange(e.target.value, setEnteredAmount, setEnteredAmountError)
                                            setError("")
                                        }}
                                        style={{minWidth: "150px"}}
                                        isInvalid={!!enteredAmountError}
                                    />
                                    <Form.Control.Feedback type="invalid">
                                        {enteredAmountError}
                                    </Form.Control.Feedback>
                                </div>
                                <Select
                                    placeholder=""
                                    styles={{
                                        control: (baseStyles, state) => ({
                                            ...baseStyles,
                                            minWidth: "80px"
                                        }),
                                    }}
                                    options={currencies}
                                    onChange={(v) => {
                                        setChosenCurrency(v["value"]);
                                        setError("")
                                    }}
                                />
                            </div>
                        </Form.Group>
                    </Row>
                    <Row style={{rowGap: "20px"}}>
                        <Form.Group as={Col} style={{minWidth: "300px"}}>
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
                                onChange={(v) => {
                                    setChosenAccount(v["value"]);
                                    setError("")
                                }}
                            />
                        </Form.Group>
                        <Col className="d-flex align-items-end justify-content-between">
                            <p className="m-0 fs-4">Total: </p>
                            {amountInAccountCurrencyIsLoading ?
                                <Spinner animation={"border"} size="sm" className={"p-2 m-1"}/> :
                                <p className="m-0 fs-4 text-nowrap">{amountInAccountCurrency ? `${chosenAccount?.currency !== chosenCurrency ? "~ " : ""}` + prettifyFloat(amountInAccountCurrency) : null} {CURRENCIES_AND_SYMBOLS[chosenAccount?.currency]}</p>
                            }
                        </Col>
                    </Row>
                    <Row>
                        <Form.Group as={Col}>
                            <Form.Label className={"little-text mb-1"}>Comment (Optional)</Form.Label>
                            <Form.Control
                                as="textarea"
                                maxLength={255}
                                value={enteredComment ? enteredComment : ''}
                                onChange={(e) => {
                                    setEnteredComment(e.target.value)
                                }}
                            />
                        </Form.Group>
                    </Row>
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <div className="d-flex justify-content-between align-items-center w-100">
                    <p className="m-0" style={{color: INTERFACE_COLORS.RED}}>{error}</p>
                    {isLoading ? <div className="mx-4"><Spinner animation="border"/></div> :
                    <div className="d-flex gap-2">
                        <Button
                            variant="secondary"
                            onClick={handleOnHide}
                        >
                            Cancel
                        </Button>
                        <Button
                            onClick={() => {
                                handleSave().then((value) => {
                                    if (value) {
                                        setHasChanged(!hasChanged)
                                        handleOnHide()
                                    }
                                }).finally(() => setIsLoading(false))
                            }}
                            variant={isRemove ? "danger" : "success"}
                        >
                            {isRemove ? "Save spending" : "Save income"}
                        </Button>
                    </div>
                    }
                </div>
            </Modal.Footer>
        </Modal>
    </>);
};

export default AddTransactionModal;