import React from 'react';
import Alert from 'react-bootstrap/Alert';

export const ErrorComponent = ({message, onClose}) => {

    if (message) {
        return (
            <Alert
                variant="danger"
                onClose={onClose}
                dismissible
                style={{
                    position: 'absolute', top: '40px', zIndex: '500', width: '25%', right: '40px'
                }}
            >
                <Alert.Heading>Error!</Alert.Heading>
                <p>
                    {message}
                </p>
            </Alert>
        );
    }
}