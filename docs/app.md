! Di awal itu (pas client buka aplikasi) harus connect dulu socket ke server

Flow register:
1. client -> input email
2. client -> `sock.send({ request: "register", email: "example@mail.com" })`
3. server -> kirim password ke email user
4. client -> `sock.recv()`
    - { message: "Check your email" }

Flow login:
1. client -> input email & password
2. client -> `sock.send({ request: "login", email: "example@mail.com", password: "123" })`
3. server -> terima (token) / tolak
4. client -> `sock.recv()`
    - pas diterima
        { token: "eyada.adasd.qweq" }
    - pas ditolak
        { token: null }

Flow finding match:
1. client -> `sock.send({ request: "find", role: "zombie", token: "eyada.adasd.qweq" })`
2. server -> bakal notify apakah ditolak / perlu waiting / udah ketemu lawan
3. client -> `sock.recv()`
    - pas ditolak
        { message: "no token provided!" }
    - pas waiting
        { match_status: "waiting" }
    - pas ketemu lawan
        { match_status: "found" }