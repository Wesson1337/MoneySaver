import React from 'react';
import {Modal} from "react-bootstrap";

const EditTransactionModal = ({show, setShow}) => {

    const handleOnHide = () => {
        setShow(false)
    }

    return (
        <Modal
            show={show}
            onHide={handleOnHide}
        >

        </Modal>
    );
};

export default EditTransactionModal;