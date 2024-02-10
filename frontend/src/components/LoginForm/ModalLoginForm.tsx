import React, {useCallback, useContext, useState} from 'react';
import {DefaultButton, Dialog, Stack, TextField} from '@fluentui/react';

import {AppStateContext} from '../../state/AppProvider';
import {getUserInfoSignin} from '../../api';

import styles from './ModalLoginForm.module.css';

interface Props {
  onDismiss: () => void;
  hidden?: boolean;
}
export const ModalLoginForm = ({onDismiss, hidden}: Props) => {
  const [user, setUser] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const appStateContext = useContext(AppStateContext);

  const handleOnChangeUser = useCallback(
    (event: React.FormEvent<HTMLInputElement | HTMLTextAreaElement>, newValue?: string) => {
      if (newValue) setUser( newValue);
    }, [setUser]
  );

  const handleOnChangePassword = useCallback(
    (event: React.FormEvent<HTMLInputElement | HTMLTextAreaElement>, newValue?: string) => {
      if (newValue) setPassword(newValue);
    }, [setPassword]
  );

  const handleSubmit = async () => {
    try {
      const userData = await getUserInfoSignin(user, password);
      appStateContext?.dispatch({ type: 'SET_USER_INFO', payload: userData });
      onDismiss();
    } catch (error: any) {
      console.error('Error de autenticación:', error.message);
      setError(error.message);
    }
  };

  return (
    <Dialog
      onDismiss={onDismiss}
      hidden={hidden}
      styles={{
        main: [{
          selectors: {
            ['@media (min-width: 480px)']: {
              maxWidth: '800px',
              background: "#fff",
              boxShadow: "0px 14px 28.8px rgba(0, 0, 0, 0.24), 0px 0px 8px rgba(0, 0, 0, 0.2)",
              borderRadius: "8px",
            }
          }
        }]
      }}
      dialogContentProps={{
        title: "Inicia Sesión",
        showCloseButton: true
      }}
    >
      <Stack verticalAlign="center" horizontalAlign="center" style={{gap: "8px", padding: "20px"}}>
        {error && (
          <p className={styles.errorMessage}>{error}</p>
        )}
        <TextField label="Usuario" className={styles.textField} onChange={handleOnChangeUser} />
        <TextField
          className={styles.textField}
          label="Password"
          type="password"
          onChange={handleOnChangePassword}
          canRevealPassword
          revealPasswordAriaLabel="Show password"
        />
        <DefaultButton
          className={styles.buttonLogin}
          text="Iniciar Sesión"
          onClick={handleSubmit}
          allowDisabledFocus
          disabled={false}
        />
      </Stack>
    </Dialog>
  );
};
