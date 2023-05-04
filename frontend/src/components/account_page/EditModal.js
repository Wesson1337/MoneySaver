import React, {useEffect, useState} from 'react';
import {Button, Col, Form, Modal, Row, Spinner} from "react-bootstrap";
import Select from "react-select";
import {ACCOUNT_TYPES, CURRENCIES_AND_SYMBOLS, INTERFACE_COLORS} from "../../utils/consts";
import {patchAccount} from "../../http/accountsAPI";

const EditModal = ({show, setShow, account, accountUpdated, setAccountUpdated}) => {
    const [enteredName, setEnteredName] = useState("")
    const [chosenType, setChosenType] = useState(null)
    const [typeOptions, setTypeOptions] = useState([])
    const [error, setError] = useState("")
    const [isLoading, setIsLoading] = useState(false)

    const handleOnHide = () => {
        setShow(false)
        setEnteredName("")
        setError("")
    }

    useEffect(() => {
        let tempOptions = []
        Object.values(ACCOUNT_TYPES).forEach((type) => {
            let newType = {}
            newType["label"] =
                <div className="d-flex align-items-center gap-2">
                    <img src={type.icon} alt="" height="25px"/>
                    <p className="m-0"
                       style={{textAlign: "left"}}>{type.name}</p>
                </div>
            newType["value"] = type
            tempOptions.push(newType)
        })
        setTypeOptions(tempOptions)
    }, [])

    const handleOnSave = async () => {
        setIsLoading(true)

        if (!enteredName || !chosenType) {
            setError("At least one field is not filled")
            return
        }

        try {
            return await patchAccount(account.id, {type: chosenType.nameForRequest, name: enteredName})
        } catch (e) {
            setError(`${e.response.data.detail || e}`)
        }
    }

    return (
        <Modal
            show={show}
            onHide={handleOnHide}
            size="lg"
        >
            <Modal.Header closeButton>
                <Modal.Title>Edit account</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    <Row>
                        <Form.Group as={Col}>
                            <Form.Label className="little-text mb-1">Name</Form.Label>
                            <Form.Control
                                value={enteredName}
                                onChange={(v) => {
                                    setEnteredName(v.target.value)
                                    setError("")
                                }}
                                maxLength={32}
                            />
                        </Form.Group>
                        <Form.Group as={Col}>
                            <Form.Label className="little-text mb-1">Type</Form.Label>
                            <Select
                                onMenuOpen={() => {
                                    setError("")
                                }}
                                options={typeOptions}
                                onChange={(v) => setChosenType(v["value"])}
                                placeholder="Select type..."
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
                            >Close</Button>
                            <Button
                                onClick={() => {
                                    handleOnSave().then((r) => {
                                        if (r) {
                                            setIsLoading(false)
                                            setAccountUpdated(!accountUpdated)
                                            handleOnHide()
                                        }
                                    }).finally(() => setIsLoading(false))
                                }}
                            >Save</Button>
                        </div>
                    }
                </div>
            </Modal.Footer>
        </Modal>
    );
};

export default EditModal;