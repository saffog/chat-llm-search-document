import React, {useContext, useState} from 'react';
import {BotRegular, CalendarLtrRegular, RealEstateFilled, PersonQuestionMarkRegular} from "@fluentui/react-icons";
import styles from "./UserInfo.module.css";
import {DefaultButton, Separator} from '@fluentui/react';
import {ModalLoginForm} from '../LoginForm';
import {AppStateContext} from '../../state/AppProvider';

export const UserInfo = () => {
  const [openLoginModal, setOpenLoginModal] = useState(false);
  const appStateContext = useContext(AppStateContext);

  const handleOpenLoginModal = () => {
    if(!appStateContext?.state.userInfo?.fullName)
      setOpenLoginModal(!openLoginModal);
    else appStateContext?.dispatch({type: 'DELETE_USER_INFO'});
  }

  return (
    <div className={styles.container}>
      {appStateContext?.state.userInfo?.email ? (
        <div className={styles.userInfo}>
          <div className={styles.userAvatar}>
            <BotRegular className={styles.iconUser} />
          </div>
          <div className={styles.userDetails}>
            <p className={styles.fullName}>{appStateContext?.state.userInfo?.fullName}</p>
            <p className={styles.email}>{appStateContext?.state.userInfo?.email}</p>
            <p className={styles.role}>{appStateContext?.state.userInfo?.role}</p>
          </div>
          <Separator styles={{
            root: {
              width: '100%',
              position: 'relative',
              '::before': {
                backgroundColor: '#a19f9d',
              },
            },
          }}/>
          <div className={styles.userDetails}>
            <CalendarLtrRegular className={styles.iconDetail} />
            <p className={styles.startDate}>Fecha de inicio</p>
            <p className={styles.fullName}>{appStateContext?.state.userInfo?.dateStart}</p>
          </div>
          <Separator styles={{
            root: {
              width: '100%',
              position: 'relative',
              '::before': {
                backgroundColor: '#a19f9d',
              },
            },
          }}/>
          <div className={styles.userDetails}>
            <RealEstateFilled className={styles.iconDetail} />
            <p className={styles.startDate}>País de residencia</p>
            <p className={styles.fullName}>{appStateContext?.state.userInfo?.country}</p>
          </div>
        </div>
      ) : (
        <div className={styles.userInfo}>
          <div className={styles.userAvatar}>
            <PersonQuestionMarkRegular className={styles.iconUser} />
          </div>
        </div>
      )}
      <DefaultButton
        className={styles.buttonLogin}
        text={appStateContext?.state.userInfo?.email ? "Cerrar Sesión" : "Iniciar Sesión"}
        onClick={handleOpenLoginModal}
        allowDisabledFocus
        disabled={false}
      />
      <ModalLoginForm onDismiss={handleOpenLoginModal} hidden={!openLoginModal} />
    </div>
  );
};
