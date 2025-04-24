// Initialize fruit_casino database
db = db.getSiblingDB('fruit_casino');

// Create collections with schema validation
db.createCollection('users', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['username', 'bankroll', 'shame_counter'],
      properties: {
        username: {
          bsonType: 'string',
          minLength: 3,
          maxLength: 50
        },
        bankroll: {
          bsonType: 'double',
          minimum: 0
        },
        shame_counter: {
          bsonType: 'int',
          minimum: 0
        },
        total_winnings: {
          bsonType: 'double',
          minimum: 0
        },
        total_losses: {
          bsonType: 'double',
          minimum: 0
        },
        favorite_game: {
          bsonType: ['string', 'null']
        },
        games_played: {
          bsonType: 'array',
          items: {
            bsonType: 'string'
          }
        }
      }
    }
  }
});

db.createCollection('game_history', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['user_id', 'game_type', 'bet_amount', 'result_amount', 'played_at'],
      properties: {
        user_id: {
          bsonType: 'string'
        },
        game_type: {
          enum: ['slots', 'roulette', 'blackjack']
        },
        bet_amount: {
          bsonType: 'double',
          minimum: 0
        },
        result_amount: {
          bsonType: 'double',
          minimum: 0
        },
        net_profit: {
          bsonType: 'double'
        },
        game_details: {
          bsonType: 'object'
        },
        played_at: {
          bsonType: 'date'
        }
      }
    }
  }
});

// Create indexes
db.users.createIndex({ "username": 1 }, { unique: true });
db.game_history.createIndex({ "user_id": 1, "game_type": 1, "played_at": -1 });

// Create initial admin user if it doesn't exist
if (db.users.countDocuments({ username: "admin" }) === 0) {
  db.users.insertOne({
    username: "admin",
    bankroll: 10000.0,
    shame_counter: 0,
    total_winnings: 0.0,
    total_losses: 0.0,
    games_played: []
  });
}
