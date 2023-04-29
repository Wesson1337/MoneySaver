import React from 'react';
import {Col, Form, Modal, Row} from "react-bootstrap";

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
                <Form>
                    <Row>
                        <Form.Group as={Col}>
                            <Form.Label className="little-text">Amount</Form.Label>
                            <Form.Control
                            />
                            <p></p>
                        </Form.Group>
                    </Row>
                </Form>
            </Modal.Body>
        </Modal>
    );
};

export default TransferModal;