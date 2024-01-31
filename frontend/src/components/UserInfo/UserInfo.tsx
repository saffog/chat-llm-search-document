import React from 'react';
import {BotRegular, CalendarLtrRegular, CopyRegular, RealEstateFilled} from "@fluentui/react-icons";
import styles from "./UserInfo.module.css";
import {DefaultButton, Dialog, Separator, Stack, TextField} from '@fluentui/react';

const UserInfo = () => {
  return (
    <div className={styles.container}>
      <div className={styles.userInfo}>
        <div className={styles.userAvatar}>
          <BotRegular className={styles.iconUser} />
        </div>
        <div className={styles.userDetails}>
          <p className={styles.fullName}>Pablo Picazo Nenufar</p>
          <p className={styles.email}>pablo@nenufar.lag</p>
          <p className={styles.role}>Fullstack Developer</p>
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
          <p className={styles.fullName}>26 de Agosto del 2021</p>
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
          <p className={styles.fullName}>Perú</p>
        </div>
      </div>
      <DefaultButton
        className={styles.buttonLogin}
        text="Iniciar Sesión"
        onClick={() => null}
        allowDisabledFocus
        disabled={false}
      />
      {/*<Dialog*/}
      {/*  onDismiss={handleSharePanelDismiss}*/}
      {/*  hidden={!isSharePanelOpen}*/}
      {/*  styles={{*/}

      {/*    main: [{*/}
      {/*      selectors: {*/}
      {/*        ['@media (min-width: 480px)']: {*/}
      {/*          maxWidth: '600px',*/}
      {/*          background: "#FFFFFF",*/}
      {/*          boxShadow: "0px 14px 28.8px rgba(0, 0, 0, 0.24), 0px 0px 8px rgba(0, 0, 0, 0.2)",*/}
      {/*          borderRadius: "8px",*/}
      {/*          maxHeight: '200px',*/}
      {/*          minHeight: '100px',*/}
      {/*        }*/}
      {/*      }*/}
      {/*    }]*/}
      {/*  }}*/}
      {/*  dialogContentProps={{*/}
      {/*    title: "Share the web app",*/}
      {/*    showCloseButton: true*/}
      {/*  }}*/}
      {/*>*/}
      {/*  <Stack horizontal verticalAlign="center" style={{gap: "8px"}}>*/}
      {/*    <TextField className={styles.urlTextBox} defaultValue={window.location.href} readOnly/>*/}
      {/*    <div*/}
      {/*      className={styles.copyButtonContainer}*/}
      {/*      role="button"*/}
      {/*      tabIndex={0}*/}
      {/*      aria-label="Copy"*/}
      {/*      onClick={handleCopyClick}*/}
      {/*      onKeyDown={e => e.key === "Enter" || e.key === " " ? handleCopyClick() : null}*/}
      {/*    >*/}
      {/*      <CopyRegular className={styles.copyButton} />*/}
      {/*      <span className={styles.copyButtonText}>{copyText}</span>*/}
      {/*    </div>*/}
      {/*  </Stack>*/}
      {/*</Dialog>*/}
    </div>
  );
};


export default UserInfo;
