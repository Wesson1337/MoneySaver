import React, {useEffect, useState} from 'react';
import MainPageCard from "./MainPageCard";
import {OPERATIONS_ROUTE} from "../utils/consts";
import dots from "../static/icons/menu-dots-vertical.svg"

const LastOperationsCard = (props) => {
    const [showModal, setShowModal] = useState(false)
    const [navigateTo, setNavigateTo] = useState(OPERATIONS_ROUTE)
    const [operations, setOperations] = useState(null)
    const [amountOfOperations, setAmountOfOperations] = useState(localStorage.getItem("amountOfOperations") || 5)
    const [isLoading, setIsLoading] = useState(true)

    const setAmountOfOperationsLocal = (amount) => {
        setAmountOfOperations(amount)
        localStorage.setItem("amountOfOperations", amount)
    }

    const uniteOperationsForCard = () => {
        let operationsArray = []
        for (let i = 0; i < amountOfOperations; i++) {
            if (props.data.operations.spendings[i]) {
                operationsArray.push(props.data.operations.spendings[i])
            }
            if (props.data.operations.incomes[i]) {
                operationsArray.push(props.data.operations.incomes[i])
            }
        }
        console.log(operationsArray)
        operationsArray.sort((a, b) => new Date(b["created_at"]) - new Date(a["created_at"]))

        console.log(operationsArray.slice(0, amountOfOperations))
    }

    useEffect(() => uniteOperationsForCard(), [])

    return (
        <MainPageCard navigateto={navigateTo} className="w-50 d-flex flex-column">
            <div className="d-flex justify-content-between align-items-center">
                <b>Last operations</b>
                <div
                    onMouseEnter={() => setNavigateTo(null)}
                    onMouseLeave={() => setNavigateTo(OPERATIONS_ROUTE)}
                    onClick={() => {
                        setShowModal(true)
                    }}
                    className="d-flex justify-content-center align-items-center"
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

            </div>
        </MainPageCard>
    );
};

export default LastOperationsCard;