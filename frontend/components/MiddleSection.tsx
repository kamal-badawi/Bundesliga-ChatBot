import React, { useEffect, useRef, useState } from 'react';
import axios from 'axios';
import TextToSpeech from './TextToSpeech';
import CopyText from './CopyText';

interface MiddleSectionProps {
  userId: string;
  conversationId: string;
  isNewChat: boolean;
}

const MiddleSection: React.FC<MiddleSectionProps> = ({ userId, conversationId, isNewChat }) => {
  const [conversations, setConversations] = useState<any[]>([]);
  const bottomRef = useRef<HTMLDivElement | null>(null);

  const fetchConversationDialog = async () => {
    try {
      let currentConversationId = conversationId;

      if (isNewChat) {
        const responseCreate = await axios.post('http://localhost:8000/create_conversation', {
          user_id: userId,
        });

        currentConversationId = responseCreate.data.conversation_id;
        console.log('Neue Konversation erstellt mit ID:', currentConversationId);
      }
      else {
      const responseDialogs = await axios.post(
        `http://localhost:8000/conversations_dialogs/${currentConversationId}`
      );
      console.log('Erhaltene Titel & IDs:', responseDialogs.data);
      setConversations(responseDialogs.data.conversations_dialogs);
      }
    } catch (error: any) {
      console.error('Fehler beim Abrufen oder Erstellen der Konversation:', error.message);
    }
  };

  useEffect(() => {
    if (userId) {
      fetchConversationDialog();
    }
  }, [userId, conversationId, isNewChat]);

  useEffect(() => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [conversations]);

  return (
    <div className="flex flex-col h-full overflow-y-auto px-4 pb-4 space-y-2">
      {conversations.map((item, index) => (
        <div key={index}>
          <div className="bg-emerald-100 text-gray-800 p-4 rounded-2xl text-right w-[35%] ml-auto mr-4 mt-10 flex flex-col">
            <div className="flex flex-row justify-between">
              <p>{item.question}</p>
              {/* Icons, TextToSpeech, CopyText können hier hinzugefügt werden */}
            </div>
          </div>

          <div className="bg-gray-100 text-gray-800 p-4 rounded-2xl text-left w-[50%] ml-4 flex flex-col space-y-2">
            <p>{item.answer}</p>
            <div className="flex gap-2">
              <TextToSpeech text={item.answer} />
              <CopyText text={item.answer} />
            </div>
          </div>
        </div>
      ))}
      <div ref={bottomRef} />
    </div>
  );
};

export default MiddleSection;
