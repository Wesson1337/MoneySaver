import React, {useState} from 'react';
import {Button, Modal, Spinner} from "react-bootstrap";
import {INTERFACE_COLORS} from "../../utils/consts";
import {deleteTransaction} from "../../http/transactionsAPI";

const DeleteTransactionModal = ({show, setShow, hasChanged, setHasChanged, transaction, type}) => {
    const [isLoading, setIsLoading] = useState(false)
    const [error, setError] = useState("")

    const handleOnSave = async () => {
        try {
            return await deleteTransaction(transaction.id, type)
        } catch (e) {
            setError(`${e?.response?.data?.detail || e}`)
        }
    }

    const handleOnHide = () => {
        setShow(false)
    }

    return (
        <Modal
            show={show}
            onHide={handleOnHide}
        >
            <Modal.Header>
                <Modal.Title>Delete transaction</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                Are you sure you want to delete the transaction?
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
                                variant="danger"
                            >
                                Delete
                            </Button>
                        </div>
                    }
                </div>
            </Modal.Footer>
        </Modal>
    );
};

export default DeleteTransactionModal;