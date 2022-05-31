Nanti di awal game:
- zombie dapet 500 matahari
- plant dapet 500 matahari
- tiap x detik, client (plant & zombie) generate 25 matahari
- winner:
    - plant: kalau berhasil bertahan 5 menit
    - zombie: standar lah ya
- State game (data)
    // data = sock.recv() // pas nerima broadcast, client harus tau message itu event apa...
    - event:
        - saat terjadi spawn zombie
            {
                event: "on_zombie_spawn",
                zombie: {
                    id: "something-unique"
                    type: "normal",
                    pos: {
                        x: 123,
                        y: 456
                    },
                    tile: {
                        x: 4,
                        y: 1
                    }
                }
            }
        - saat terjadi spawn tanaman
            {
                event: "on_plant_spawn",
                plant: {
                    id: "something-unique"
                    type: "normal",
                    pos: {
                        x: 123,
                        y: 456
                    },
                    tile: {
                        x: 4,
                        y: 1
                    }
                }
            }
        - saat zombie berubah posisi (zombie lagi jalan)
            {
                event: "on_zombie_move",
                zombie: {
                    id: "something-unique"
                    pos: {
                        x: 123,
                        y: 456
                    },
                    tile: {
                        x: 4,
                        y: 1
                    }
                }
            }
        - saat zombie melakukan serangan ke tanaman (zombie lagi makan)
            {
                event: "on_zombie_attack",
                zombie: {
                    id: "unique"
                }
                plant: {
                    id: "unique"
                }
            }
        - saat zombie mati
            {
                event: "on_zombie_die",
                zombie: {
                    id: "unique"
                }
            }
        - saat tanaman mati
            {
                event: "on_plant_die",
                plant: {
                    id: "unique"
                }
            }
        - saat tanaman mulai menembak peluru
            {
                event: "on_plant_shoot",
                plant: {
                    id: "unique"
                }
            }
        - saat tanaman melakukan serangan ke zombie
            {
                event: "on_plant_attack",
                zombie: {
                    id: "unique"
                }
                plant: {
                    id: "unique"
                }
            }
        - saat sudah ada pemenang (plant / zombie)
            {
                event: "on_winner",
                winner: "zombie" // bisa juga plant
            }

Jenis zombie ?
1. normal - price: 50
2. cone - price: 100
3. bucket - price: 200

Jenis plant ?
1. pea - price: 100
2. repeater (shooter yang 2x nembak) - price: 200
3. potato - price: 250