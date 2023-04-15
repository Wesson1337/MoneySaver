import React from 'react';

const Sort = ({children, by}) => {
    const compare = (a, b) => {
        return b.props[by] - a.props[by]
    }

    if (!by) {
        return children
    }

    return React.Children.toArray(children).sort(compare)
};

export default Sort;