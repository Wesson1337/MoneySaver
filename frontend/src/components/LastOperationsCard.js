import React, {useEffect, useState} from 'react';
import MainPageCard from "./MainPageCard";
import {OPERATIONS_ROUTE} from "../utils/consts";
import dots from "../static/icons/menu-dots-vertical.svg"
import {Spinner} from "react-bootstrap";
import Operation from "./Operation";

const LastOperationsCard = (props) => {
    const [showModal, setShowModal] = useState(false)
    const [navigateTo, setNavigateTo] = useState(OPERATIONS_ROUTE)
    const [operations, setOperations] = useState(null)
    const [amountOfOperations, setAmountOfOperations] = useState(5)
    const [isLoading, setIsLoading] = useState(true)

    const setAmountOfOperationsLocal = (amount) => {
        setAmountOfOperations(amount)
        localStorage.setItem("amountOfOperations", amount)
    }

    const checkAmountOfOperations = () => {
        const amount = Number(localStorage.getItem("amountOfOperations"))
        if (!Number.isInteger(amount) || amount < 1 || amount > 20) {
            setAmountOfOperationsLocal(5)
        } else {
            setAmountOfOperations(amount)
        }
    }


    const uniteOperationsForCard = () => {
        checkAmountOfOperations()
        let operationsArray = []
        for (let i = 0; i < amountOfOperations; i++) {
            if (props.data.operations.spendings[i]) {
                operationsArray.push(props.data.operations.spendings[i])
            }
            if (props.data.operations.incomes[i]) {
                operationsArray.push(props.data.operations.incomes[i])
            }
        }
        operationsArray.sort((a, b) => new Date(b["created_at"]) - new Date(a["created_at"]))
        setOperations(operationsArray.slice(0, amountOfOperations))
        setIsLoading(false)
    }

    useEffect(() => {
        uniteOperationsForCard()
    }, [])

    return (
        <MainPageCard navigateto={navigateTo} className="w-50 d-flex flex-column">
            {isLoading
                ?
                <div className="d-flex justify-content-center"><Spinner variant="border"/></div>
                :
                <>
                    <div className="d-flex justify-content-between align-items-center">
                        <b>Last operations</b>
                        <div
                            onMouseEnter={() => setNavigateTo(null)}
                            onMouseLeave={() => setNavigateTo(OPERATIONS_ROUTE)}
                            onClick={() => {
                                setShowModal(true)
                            }}
                            className="d-flex justify-content-end align-items-center"
                            style={{
                                width: "24px",
                                height: "24px",
                                cursor: "pointer",
                            }}>
                            <img
                                src={dots} alt={""} height={15} style={{
                                filter: navigateTo ? null : "drop-shadow(1px 1px 1px rgba(2, 2, 2, 0.5))",
                                transition: "0.25s"
                            }}/>
                        </div>
                    </div>
                    <div className="w-100">
                        {operations.map(o =>
                            <Operation
                                key={o.id}
                                name={o.name}
                                type={o["category"] ? "spending" : "income"}
                                category={o["category"] ? o["spending_category"] : o["name"]}
                                date={o["created_at"]}
                                account={o["category"] ? o["receipt_account"] : o["replenishment_account"]}
                        />)}
                    </div>
                </>}
        </MainPageCard>
    );
};

export default LastOperationsCard;