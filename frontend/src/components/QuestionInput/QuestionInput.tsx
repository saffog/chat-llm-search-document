import { useState } from "react";
import { Stack, TextField } from "@fluentui/react";
import { SendRegular } from "@fluentui/react-icons";
import Send from "../../assets/Send.svg";
import styles from "./QuestionInput.module.css";

interface Props {
    onSend: (question: string, roleValue?: string, id?: string) => void;
    disabled: boolean;
    placeholder?: string;
    rolePlaceHolder?: string;
    clearOnSend?: boolean;
    conversationId?: string;
    showRoleInput?: boolean;
}

export const QuestionInput = ({ onSend, disabled, placeholder, rolePlaceHolder, clearOnSend, conversationId, showRoleInput }: Props) => {
    const [question, setQuestion] = useState<string>("");
    const [roleValue, setRoleValue] = useState<string>("");

    const sendQuestion = () => {
        if (disabled || !question.trim()) {
            return;
        }
        console.log("Sending question:", question, "roleValue:", roleValue, "conversationId:", conversationId);

        if(conversationId && roleValue){
            onSend(question, roleValue, conversationId);
        }else{
            if (conversationId) {
                onSend(question, undefined, conversationId);
            } else if (roleValue) {
                onSend(question, roleValue, undefined);                
            } else {
                onSend(question);
            }
        }

        if (clearOnSend) {
            setQuestion("");
        }
    };

    const onEnterPress = (ev: React.KeyboardEvent<Element>) => {
        if (ev.key === "Enter" && !ev.shiftKey) {
            ev.preventDefault();
            sendQuestion();
        }
    };

    const onQuestionChange = (_ev: React.FormEvent<HTMLInputElement | HTMLTextAreaElement>, newValue?: string) => {
        setQuestion(newValue || "");
    };

    const onRoleChange = (_ev: React.FormEvent<HTMLInputElement | HTMLTextAreaElement>, newValue?: string) => {
        setRoleValue(newValue || "");
    }

    const sendQuestionDisabled = disabled || !question.trim();

    return (
        <Stack horizontal className={styles.questionInputContainer}>
            {showRoleInput && (<TextField 
                className={styles.questionInputTextArea} 
                placeholder={rolePlaceHolder} 
                multiline 
                resizable={false}
                value={roleValue} 
                onChange={onRoleChange} />
                )}
            <TextField
                className={styles.questionInputTextArea}
                placeholder={placeholder}
                multiline
                resizable={false}
                borderless
                value={question}
                onChange={onQuestionChange}
                onKeyDown={onEnterPress}
            />
            <div className={styles.questionInputSendButtonContainer} 
                role="button" 
                tabIndex={0}
                aria-label="Ask question button"
                onClick={sendQuestion}
                onKeyDown={e => e.key === "Enter" || e.key === " " ? sendQuestion() : null}
            >
                { sendQuestionDisabled ? 
                    <SendRegular className={styles.questionInputSendButtonDisabled}/>
                    :
                    <img src={Send} className={styles.questionInputSendButton}/>
                }
            </div>
            <div className={styles.questionInputBottomBorder} />
        </Stack>
    );
};
