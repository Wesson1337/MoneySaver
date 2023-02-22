import React from 'react';
import Alert from 'react-bootstrap/Alert';

export const ErrorComponent = (props) => {

  if (props.message) {
    return (
      <Alert
          variant="danger"
          onClose={props.onClose}
          dismissible
          style={{
            position: 'absolute', top: '40px', zIndex: '500', width: '25%', right: '40px'
      }}
      >
        <Alert.Heading>Error!</Alert.Heading>
        <p>
            {props.message}
        </p>
      </Alert>
    );
  }
}