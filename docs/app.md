> Di awal itu (pas client buka aplikasi) harus connect dulu socket ke server

---

## Flow register:

1. client -> input email
2. client -> `sock.send({ request: "register", email: "example@mail.com" })`
3. server -> kirim password ke email user
4. client -> `sock.recv()`
   - success
     - `{ success: true, message: "Check your email" }`
   - failed
     - `{ success: false, message: "Email is invalid!" }`
     - `{ success: false, message: "Email is already registered!" }`

---

## Flow login:

1. client -> input email & password
2. client -> `sock.send({ request: "login", email: "example@mail.com", password: "123" })`
3. server -> terima (token) / tolak
4. client -> `sock.recv()`
   - success
     - `{ success: true, token: "eyada.adasd.qweq" }`
   - failed
     - `{ success: false, message: "Email and password are required!" }`
     - `{ success: false, message: "Email is not registered!" }`
     - `{ success: false, message: "Wrong password!" }`

---

## Flow finding match:

1. client -> `sock.send({ request: "find", role: "zombie", token: "eyada.adasd.qweq" })`
2. server -> bakal notify apakah ditolak / perlu waiting / udah ketemu lawan
3. client -> `sock.recv()`
   - success
     - `{ success: true, match_status: "waiting" }`
     - `{ success: true, match_status: "found", enemy: "someuser@mail.com" }`
   - failed
     - `{ success: false, message: "Token is required!" }`
     - `{ success: false, message: "Invalid token!" }`
     - `{ success: false, message: "Role should be plant or zombie" }`
     - `{ success: false, message: "You are already in queue" }`
