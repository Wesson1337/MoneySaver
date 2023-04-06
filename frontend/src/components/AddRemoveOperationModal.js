import React, {useEffect, useState} from 'react';
import {Col, Form, Modal, Row} from "react-bootstrap";
import {CURRENCIES_AND_SYMBOLS, INCOME_CATEGORIES, SPENDING_CATEGORIES} from "../utils/consts";
import Select from "react-select";

const AddRemoveOperationModal = ({show, setShow, type}) => {
    const isRemove = type === "remove"
    const [categories, setCategories] = useState(null)
    const [currencies, setCurrencies] = useState(null)
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

    const [chosenCategory, setChosenCategory] = useState(null)
    const [enteredAmount, setEnteredAmount] = useState(null)
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
                <Form>
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
                                />


                            </div>
                        </Form.Group>
                    </Row>
                </Form>
            </Modal.Body>
        </Modal>
    </>);
};

export default AddRemoveOperationModal;