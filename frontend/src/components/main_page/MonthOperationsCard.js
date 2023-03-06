import React from 'react';
import MainPageCard from "./MainPageCard";
import {OPERATIONS_ROUTE} from "../../utils/consts";

const MonthOperationsCard = (props) => {
    return (
        <MainPageCard navigateTo={OPERATIONS_ROUTE}>
        </MainPageCard>
    );
};

export default MonthOperationsCard;