import { io, Socket } from 'socket.io-client';

const URL = 'http://localhost:8000'; // Assuming the backend is running on port 8000

class SocketService {
    private socket: Socket;

    constructor(token: string) {
        this.socket = io(URL, {
            // auth: {
            //     token: `Bearer ${token}`
            // },
            // extraHeaders: {
            //     Authorization: `Bearer ${token}`
            // }
        });
    }

    getSocket(): Socket {
        return this.socket;
    }
}

export default SocketService;
