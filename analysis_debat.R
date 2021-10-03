# Title     : TODO
# Objective : TODO
# Created by: user
# Created on: 2021-10-03

pkg_fun <- function(pkg) {
  if (!require(pkg, character.only = TRUE)) {
    install.packages(pkg)
    library(pkg, character.only = TRUE)
  }
}
Sys.setlocale("LC_CTYPE", ".1251")

pkg_fun("mongolite")
pkg_fun("dplyr")
pkg_fun("readr")
pkg_fun("stringr")
pkg_fun("tidytext")
pkg_fun("textclean")

dic <- read_csv("knu_sentiment_lexicon.csv")

newdb <- mongo(collection = "comment",
               db = "stock",
               url = "mongodb://localhost",
               verbose = TRUE)

word_raw <- newdb$find()
word_raw <- word_raw$comment
word_raw <-as_tibble(word_raw)

# dic %>% filter(polarity == 2) %>% arrange(word)
# dic %>% filter(polarity == -2) %>% arrange(word)
word <- word_raw %>% unnest_tokens(input=value,output = word, token="words",drop = F)
word <- word %>% left_join(dic,by="word") %>% mutate(polarity=ifelse(is.na(polarity),0,polarity))

score <- word %>% group_by(value) %>% summarise(score = sum(polarity))