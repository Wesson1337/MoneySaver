import React from 'react';
import {Modal} from "react-bootstrap";

const TransferModal = ({show, setShow}) => {
    const handleClose = () => {
        setShow(false)
    }
    return (
        <Modal
            show={show}
            onHide={handleClose}
        >
            <Modal.Header
                closeButton
            >
                <Modal.Title>Transfer between accounts</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                
            </Modal.Body>
        </Modal>
    );
};

export default TransferModal;