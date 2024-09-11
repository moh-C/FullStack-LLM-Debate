import axios from 'axios';

const API_URL = 'http://localhost:8000';

const testEndpoint = async (endpoint, method = 'get', data = null) => {
    try {
        let response;
        if (method === 'get') {
            response = await axios.get(`${API_URL}${endpoint}`);
        } else if (method === 'post') {
            response = await axios.post(`${API_URL}${endpoint}`, data);
        }
        console.log(`${endpoint} response:`, response);
        return response.data;
    } catch (error) {
        console.error(`Error from ${endpoint}:`, error.response || error);
        return null;
    }
};

export const startDebate = async (debateData) => {
    const response = await testEndpoint('/start_debate', 'post', debateData);
    return response && response.message.includes("Debate initialized") ? response : null;
};

export const oneTurnDebate = async () => {
    return await testEndpoint('/one_turn_debate', 'post');
};

export const fetchPersonas = async () => {
    return await testEndpoint('/personas', 'get');
};

export const fetchDebateHistory = async () => {
    return await testEndpoint('/debate_history', 'get');
};

export const getDebate = async (debateId) => {
    return await testEndpoint(`/debate/${debateId}`, 'get');
};

export const getHealth = async () => {
    return await testEndpoint('/health', 'get');
};

export const sendWebSocketMessage = (ws, message) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify(message));
    } else {
        console.error('WebSocket is not open');
    }
};