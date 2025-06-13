import React, { useState } from 'react';
import axios from 'axios';



const ConversationsMenu = () => {
  const [conversationsTitles, setConversationsTitles] = useState<string[]>([])

  const getConversationsTitles = async ()=>{
    try{
    const response = await axios.get('http://127.0.0.1:8000/conversations_titles');
    if (response.status === 200){
      
  
    }
  
  }
  catch (error){
    console.error('Fehler beim Hooen der Koversationstiteln:', error);
  
  }
  }
  return (
    <div>
      {conversationsTitles.map((item, index) => (
        <div key={index}>{item}</div>
      ))}
    </div>
  );
};

export default ConversationsMenu;
