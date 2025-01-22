#!/bin/bash

set -e

wait_for_elasticsearch() {
  echo "Waiting for Elasticsearch to start..."
  until curl -s "http://elasticsearch:9200/_cat/health?h=status" | grep -E -q "(yellow|green)"; do
    sleep 2
  done
  echo "Elasticsearch started."
}

create_movies_index() {
  local index_name="$1"

  local index_exists
  index_exists=$(curl -s -o /dev/null -w "%{http_code}" "http://elasticsearch:9200/${index_name}")

  if [ "$index_exists" -ne 200 ]; then
    echo "Creating index '${index_name}'..."

    curl -XPUT "http://elasticsearch:9200/${index_name}" \
      -H "Content-Type: application/json" \
      -d'
      {
        "settings": {
          "refresh_interval": "1s",
          "analysis": {
            "filter": {
              "english_stop": {
                "type": "stop",
                "stopwords": "_english_"
              },
              "english_stemmer": {
                "type": "stemmer",
                "language": "english"
              },
              "english_possessive_stemmer": {
                "type": "stemmer",
                "language": "possessive_english"
              },
              "russian_stop": {
                "type": "stop",
                "stopwords": "_russian_"
              },
              "russian_stemmer": {
                "type": "stemmer",
                "language": "russian"
              }
            },
            "analyzer": {
              "ru_en": {
                "tokenizer": "standard",
                "filter": [
                  "lowercase",
                  "english_stop",
                  "english_stemmer",
                  "english_possessive_stemmer",
                  "russian_stop",
                  "russian_stemmer"
                ]
              }
            }
          }
        },
        "mappings": {
          "dynamic": "strict",
          "properties": {
            "id": {
              "type": "keyword"
            },
            "imdb_rating": {
              "type": "float"
            },
            "genres": {
              "type": "keyword"
            },
            "title": {
              "type": "text",
              "analyzer": "ru_en",
              "fields": {
                "raw": {
                  "type": "keyword"
                }
              }
            },
            "description": {
              "type": "text",
              "analyzer": "ru_en"
            },
            "directors_names": {
              "type": "text",
              "analyzer": "ru_en"
            },
            "actors_names": {
              "type": "text",
              "analyzer": "ru_en"
            },
            "writers_names": {
              "type": "text",
              "analyzer": "ru_en"
            },
            "directors": {
              "type": "nested",
              "dynamic": "strict",
              "properties": {
                "id": {
                  "type": "keyword"
                },
                "name": {
                  "type": "text",
                  "analyzer": "ru_en"
                }
              }
            },
            "actors": {
              "type": "nested",
              "dynamic": "strict",
              "properties": {
                "id": {
                  "type": "keyword"
                },
                "name": {
                  "type": "text",
                  "analyzer": "ru_en"
                }
              }
            },
            "writers": {
              "type": "nested",
              "dynamic": "strict",
              "properties": {
                "id": {
                  "type": "keyword"
                },
                "name": {
                  "type": "text",
                  "analyzer": "ru_en"
                }
              }
            }
          }
        }
      }'
    echo "Index '${index_name}' created successfully."
  else
    echo "Index '${index_name}' already exists. Skipping index creation."
  fi
}

wait_for_elasticsearch
create_movies_index
python /opt/app/main.py
