import React, {useEffect, useState} from 'react';
import {Button, Col, Form, Modal, Row, Spinner} from "react-bootstrap";
import Select from "react-select";
import {CURRENCIES_AND_SYMBOLS, INCOME_CATEGORIES, INTERFACE_COLORS, SPENDING_CATEGORIES} from "../../utils/consts";
import {handleAmountOnChange} from "../../utils/forms"
import {patchTransaction} from "../../http/transactionsAPI";

const EditTransactionModal = ({show, setShow, hasChanged, setHasChanged, transaction, type, account}) => {
    const [enteredComment, setEnteredComment] = useState("")
    const [enteredAmount, setEnteredAmount] = useState(transaction.amount)
    const [enteredAmountError, setEnteredAmountError] = useState("")
    const [error, setError] = useState("")
    const [isLoading, setIsLoading] = useState(false)
    const [categories, setCategories] = useState([])
    const [chosenCategory, setChosenCategory] = useState(null)

    useEffect(() => {
        let tempCategories = []
        Object.entries(type === "spending" ? SPENDING_CATEGORIES : INCOME_CATEGORIES).forEach(([key, category]) => {
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

    const handleOnSave = async () => {
        setIsLoading(true)

        if (!enteredAmount && !chosenCategory && !enteredComment) {
            setError("At least one field must be filled")
            return
        }
        if (type === "spending" && transaction["amount_in_account_currency_at_creation"] > account) {
            setError("After this spending account balance will go negative")
            return
        }

        try {
            return await patchTransaction(transaction.id, type, {
                amount: enteredAmount ? enteredAmount : null,
                category: chosenCategory?.nameForRequest,
                comment: enteredComment ? enteredComment : null
            })
        } catch (e) {
            setError(`${e?.response?.data?.detail || e}`)
        }
    }

    const handleOnHide = () => {
        setShow(false)
        setEnteredAmount(transaction.amount)
        setEnteredComment("")
        setEnteredAmountError("")
        setError("")
        setChosenCategory(null)
    }

    return (
        <Modal
            show={show}
            onHide={handleOnHide}
            size="lg"
        >
            <Modal.Header
                closeButton
            >
                <Modal.Title>Edit transaction</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    <Row>
                        <Form.Group as={Col}>
                            <Form.Label className="little-text mb-1">Amount</Form.Label>
                            <div className="d-flex flex-column w-100">
                                <div className="d-flex flex-row justify-content-center align-items-center gap-2">
                                    <Form.Control
                                        value={enteredAmount ? enteredAmount : ''}
                                        onChange={(e) => {
                                            handleAmountOnChange(e.target.value, setEnteredAmount, setEnteredAmountError)
                                            setError("")
                                        }}
                                        style={{minWidth: "150px"}}
                                        isInvalid={!!enteredAmountError}
                                    />
                                    <p className="m-0">{CURRENCIES_AND_SYMBOLS[transaction.currency]}</p>
                                </div>
                                <Form.Control.Feedback type="invalid">
                                    {enteredAmountError}
                                </Form.Control.Feedback>
                            </div>
                        </Form.Group>
                        <Form.Group as={Col}>
                            <Form.Label className="little-text mb-1">Category</Form.Label>
                            <Select
                                placeholder="Select category..."
                                onChange={(v) => {
                                    setChosenCategory(type === "spending" ? SPENDING_CATEGORIES[v["value"]] : INCOME_CATEGORIES[v["value"]])
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
                    </Row>
                    <Row>
                        <Form.Group as={Col}>
                            <Form.Label className="little-text mb-1">Comment</Form.Label>
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
                                    handleOnSave().then((value) => {
                                        if (value) {
                                            setHasChanged(!hasChanged)
                                            handleOnHide()
                                        }
                                    }).finally(() => setIsLoading(false))
                                }}
                                variant={type === "spending" ? "danger" : "success"}
                            >
                                {type === "spending" ? "Save spending" : "Save income"}
                            </Button>
                        </div>
                    }
                </div>
            </Modal.Footer>
        </Modal>
    );
};

export default EditTransactionModal;