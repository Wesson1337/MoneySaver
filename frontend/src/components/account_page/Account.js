import React, {useState} from 'react';
import {Card, Form} from "react-bootstrap";
import {ACCOUNT_TYPES, CURRENCIES_AND_SYMBOLS} from "../../utils/consts";
import {prettifyFloat} from "../../utils/prettifyFloat";
import transferIcon from "../../static/icons/transfer-svgrepo-com.svg"
import editIcon from "../../static/icons/edit-svgrepo-com.svg"
import eyeIcon from "../../static/icons/eye-open-svgrepo-com.svg"

const Account = ({account, index}) => {
    const [isExpanded, setIsExpanded] = useState(false)


    const handleCheckOnChange = async () => {

    }

    return (
        <Card
            className="p-3 d-flex flex-column gap-2"
            style={{
                height: isExpanded ? "135px" : "99.34px",
                transition: "0.25s ease-out"
            }}
        >
            <div className="d-flex justify-content-between align-items-center">
                <p className="m-0">{account.name}</p>
                <p className="m-0 text-nowrap">{prettifyFloat(account.balance.toFixed(2))} {CURRENCIES_AND_SYMBOLS[account.currency]}</p>
            </div>
            <div className="d-flex justify-content-between align-items-center">
                <Form>
                    <Form.Check
                        id={`account-checkbox-${index !== undefined ? index : 1}`}
                        label={"Active"}
                        type={"switch"}
                        defaultChecked={account["is_active"]}
                    />
                </Form>
                <div
                    className="d-flex gap-2"
                >
                    <div
                        className="account-action"
                        onClick={() => {
                            setIsExpanded(!isExpanded)
                        }}
                    >
                        <img
                            src={eyeIcon}
                            width={27}
                            alt=""
                        />
                    </div>
                    <div
                        className="account-action"
                    >
                        <img
                            src={transferIcon}
                            width={27}
                            alt=""
                        />
                    </div>
                    <div
                        className="account-action"
                    >
                        <img
                            src={editIcon}
                            width={27}
                            alt=""
                        />
                    </div>
                </div>
            </div>
            <div className="d-flex justify-content-between mt-1">
                <p
                    className="m-0"
                    style={{transition: "0.15s ease-out", color: isExpanded ? "black" : "transparent"}}
                >Type: {ACCOUNT_TYPES[account["type"]].name}</p>
                <p
                    className="m-0"
                    style={{transition: "0.15s ease-out", color: isExpanded ? "black" : "transparent"}}
                >Balance in USD: {prettifyFloat(account["balanceInUSD"].toFixed(2))} $</p>
            </div>
        </Card>
    );
};

export default Account;