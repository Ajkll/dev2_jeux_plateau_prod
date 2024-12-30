CREATE TABLE scores ( -- Pourrais etre if not existe pour eviter les logs d'erreurs
    id SERIAL PRIMARY KEY,
    pseudo VARCHAR(255) NOT NULL,
    score_total INTEGER NOT NULL,
    date_partie TIMESTAMP NOT NULL
);
-- ajouter logique pour les utilisateur ect (pas le temps)