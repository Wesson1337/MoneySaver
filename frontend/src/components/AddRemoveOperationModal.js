import React, {useState} from 'react';
import {Button, Dropdown, Modal} from "react-bootstrap";
import {INCOME_CATEGORIES, SPENDING_CATEGORIES} from "../utils/consts";

const AddRemoveOperationModal = ({show, setShow, type}) => {
    const CustomToggle = React.forwardRef(({children, onClick}, ref) => (
        <Button
            variant="outline-secondary"
            ref={ref}
            onClick={(e) => {
                e.preventDefault();
                onClick(e);
            }}
            className="btn-categories"
        >
            <div className="d-flex justify-content-between align-items-center gap-2">
                {chosenCategory ?
                    <>
                        <img src={chosenCategory.icon} alt="" height="25px"/>
                        <p className="m-0">{chosenCategory.name}</p>
                    </>
                    :
                    <p className="m-0">Choose category</p>
                }
                <b style={{
                    width: 0,
                    height: 0,
                    borderLeft: "5px solid transparent",
                    borderRight: "5px solid transparent",
                    borderTop: "5px solid #6c757d"
                }}/>
            </div>
        </Button>
    ));

    const [chosenCategory, setChosenCategory] = useState(null)
    return (
        <>
            <Modal
                show={show}
                onHide={() => {
                    setChosenCategory(null)
                    setShow(false)
                }}
                backdrop="static"
                keyboard={false}
            >
                <Modal.Header closeButton>
                    <Modal.Title>New {type === "remove" ? "spending" : "income"}</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Dropdown>
                        <Dropdown.Toggle as={CustomToggle}>Custom toggle</Dropdown.Toggle>
                        <Dropdown.Menu>
                            {Object.values(type === "remove" ? SPENDING_CATEGORIES : INCOME_CATEGORIES).map((category) => (
                                <Dropdown.Item
                                    key={category.name}
                                    onClick={() => {
                                        setChosenCategory(category)
                                    }}
                                    className="dropdown-categories"
                                >
                                    <div className="d-flex justify-content-between align-items-center gap-2">
                                        <img src={category.icon} alt="" height="25px"/>
                                        <p className="m-0" style={{minWidth: "145.13px"}}>{category.name}</p>
                                    </div>
                                </Dropdown.Item>
                            ))}
                        </Dropdown.Menu>
                    </Dropdown>
                </Modal.Body>
            </Modal>
        </>
    );
};

export default AddRemoveOperationModal;