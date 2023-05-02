import React from 'react';
import {Button, Col, Form, Modal, Row} from "react-bootstrap";
import Select from "react-select";

const EditModal = ({show, setShow}) => {
    const handleOnHide = () => {
        setShow(false)
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
                                maxLength={255}
                            />
                        </Form.Group>
                        <Form.Group as={Col}>
                            <Form.Label className="little-text mb-1">Type</Form.Label>
                            <Select
                                
                            />
                        </Form.Group>
                    </Row>
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button
                    variant="secondary"
                    onClick={handleOnHide}
                >Close</Button>
                <Button>Save</Button>
            </Modal.Footer>
        </Modal>
    );
};

export default EditModal;