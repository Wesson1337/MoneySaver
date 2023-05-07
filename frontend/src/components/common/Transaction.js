import React, {useState} from 'react';
import {CURRENCIES_AND_SYMBOLS, INTERFACE_COLORS, TRANSACTIONS_ROUTE} from "../../utils/consts";
import {prettifyFloat} from "../../utils/prettifyFloat";
import dots from "../../static/icons/menu-dots-vertical.svg"
import {useLocation} from "react-router-dom";
import {Dropdown} from "react-bootstrap";
import EditTransactionModal from "../transactions_page/EditTransactionModal";
import DeleteTransactionModal from "../transactions_page/DeleteTransactionModal";

const Transaction = ({
                         icon, transaction, hasChanged, setHasChanged, type, account, category
                     }) => {
    const [showEditModal, setShowEditModal] = useState(false)
    const [showDeleteModal, setShowDeleteModal] = useState(false)
    const location = useLocation()
    const isTransactionPage = location.pathname === TRANSACTIONS_ROUTE
    return (
        <div className="d-flex gap-2 align-items-center">
            <img
                src={icon}
                style={{height: "40px"}}
                alt=""
            />
            <div className="w-100">
                <div className="d-flex justify-content-between align-items-center gap-3">
                    <p className="m-0 little-text text-nowrap">
                        {category}
                    </p>
                    <p className="m-0 little-text text-nowrap">
                        {type === "spending" ? "-" : "+"}{transaction.amount !== transaction["amount_in_account_currency_at_creation"] ? prettifyFloat(transaction["amount_in_account_currency_at_creation"].toFixed(2)) : prettifyFloat(transaction.amount.toFixed(2))} {CURRENCIES_AND_SYMBOLS[account.currency]}
                    </p>
                </div>
                <div className="d-flex justify-content-between align-items-center gap-3">
                    <p className="m-0 little-text">
                        {`${account["name"] ? `${account["name"].substring(0, 12)}${account.name.length > 12 ? "..." : ""}` : "Unnamed account"}`}
                    </p>
                    <p className="m-0 little-text text-nowrap">
                        {new Date(transaction["created_at"]).toLocaleDateString("ru-RU", {
                            hour: "2-digit",
                            minute: "2-digit"
                        })}
                    </p>
                </div>
            </div>
            {isTransactionPage ?
                <>
                    <Dropdown>
                        <Dropdown.Toggle
                            className="d-flex justify-content-center align-items-center transaction-three-dots"
                        >
                            <img
                                src={dots}
                                alt=""
                                width={20}
                            />
                            <Dropdown.Menu>
                                <Dropdown.Item onClick={() => setShowEditModal(true)}>
                                    Edit transaction
                                </Dropdown.Item>
                                <Dropdown.Item onClick={() => setShowDeleteModal(true)}>
                                    Delete transaction
                                </Dropdown.Item>
                            </Dropdown.Menu>
                        </Dropdown.Toggle>
                    </Dropdown>
                    <EditTransactionModal
                        show={showEditModal}
                        setShow={setShowEditModal}
                        hasChanged={hasChanged}
                        setHasChanged={setHasChanged}
                        transaction={transaction}
                        type={type}
                        account={account}
                    />
                    <DeleteTransactionModal show={showDeleteModal} setShow={setShowDeleteModal}/>
                </>
                : null
            }
            <div style={{
                width: "5px",
                height: "40px",
                background: type === "spending" ? INTERFACE_COLORS.RED : INTERFACE_COLORS.GREEN
            }}>

            </div>
        </div>
    );
};

export default Transaction;