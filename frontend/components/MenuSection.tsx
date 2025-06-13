import React from 'react';
import axios from 'axios';

interface MenuSectionProps {
  userId: string;
  conversationsTitles: any[];
  setConversationsTitles: React.Dispatch<React.SetStateAction<any[]>>;
  searchTerm: string;
  setSearchTerm: React.Dispatch<React.SetStateAction<string>>;
  setConversationId: React.Dispatch<React.SetStateAction<string>>;
  setIsNewChat: React.Dispatch<React.SetStateAction<boolean>>;
}

const MenuSection: React.FC<MenuSectionProps> = ({
  userId,
  conversationsTitles,
  setConversationsTitles,
  searchTerm,
  setSearchTerm,
  setConversationId,
  setIsNewChat
  
}) => {
  const openThisConversation = (id: string) => {
    setIsNewChat(false);
    setConversationId(id);
  };

  const deleteThisConversation = async (conversation_id: string) => {
    try {
      await axios.delete('http://localhost:8000/delete_conversation_by_user_and_conversation_id', {
        data: {
          user_id: userId,
          conversation_id: conversation_id,
        },
      });

      setConversationsTitles((prevConversations) =>
        prevConversations.filter((conv) => conv.conversation_id !== conversation_id)
      );
    } catch (error: any) {
      if (error.response?.status === 404) {
        console.error('Keine Gesprächstitel gefunden.');
      } else {
        console.error('Fehler beim Löschen der Unterhaltung:', error.message);
      }
    }
  };

  return (
    <div className="w-full h-full bg-yellow-50 text-black flex flex-col overflow-hidden">

      {/* Suchfeld */}
      <div className="pt-45 border-b border-black">
        <div className="relative">
          <span className="absolute inset-y-0 left-3 flex items-center text-gray-400">
            <svg xmlns="http://www.w3.org/2000/svg"
                 fill="none" viewBox="0 0 24 24"
                 strokeWidth="1.5" stroke="currentColor"
                 className="w-5 h-5">
              <path strokeLinecap="round" strokeLinejoin="round"
                    d="m21 21-5.197-5.197M15.803 15.803A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"/>
            </svg>
          </span>
          <input
            type="text"
            placeholder="Suche..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 rounded-lg bg-gray-200 text-black placeholder-gray-500 border border-black focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
        </div>
      </div>

      {/* Gesprächstitel */}
      <div className="flex-1 overflow-y-auto px-4 py-3 space-y-2">
        {conversationsTitles.length === 0 ? (
          <p className="text-gray-500 italic">Keine Gespräche</p>
        ) : (
          conversationsTitles.map((conv, index) => (
            <div
              key={index}
              className="group flex items-center justify-between bg-gray-200 hover:bg-gray-100 rounded-lg px-4 py-3 transition cursor-pointer"
            >
              <div
                className="flex-1 truncate text-left"
                onClick={() => 
                  
                  openThisConversation(conv.conversation_id)}
              >
                {conv.title || 'Kein Titel'}
              </div>
              <button
                className="ml-3 text-gray-400 hover:text-red-600 p-1 transition"
                onClick={() => deleteThisConversation(conv.conversation_id)}
              >
                <svg xmlns="http://www.w3.org/2000/svg"
                     fill="none" viewBox="0 0 24 24"
                     strokeWidth="1.5" stroke="currentColor"
                     className="w-5 h-5">
                  <path strokeLinecap="round" strokeLinejoin="round"
                        d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21a48.11 48.11 0 0 0-3.478-.397m-12 .562a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.96 51.96 0 0 0-3.32 0c-1.18.037-2.09 1.021-2.09 2.201v.916" />
                </svg>
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default MenuSection;
