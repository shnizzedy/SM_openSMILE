library(jsonlite)
library(stringr)
library(e1071)
setwd("/Users/jon.clucas/PMAV/Watson")

files <- list.files('.', "*.json")
lists <- NULL
headers <- NULL

j = 1
for(i in 1:length(files)){
  fp <- file.path(paste(getwd(),files[i],sep="/"))
  if(str_detect(files[i], "Watson")){
    lists[j] <- strsplit(fromJSON(txt = fp)$results$alternatives[[1]]$transcript, " ")
    if(length(fromJSON(txt = fp)$results$alternatives) > 1){
      for(k in 2:length(fromJSON(txt = fp)$results$alternatives)){
        lists[[j]] <- c(lists[[j]], strsplit(fromJSON(txt = fp)$results$alternatives[[k]]$transcript, " ")[[1]])
      }
    }
    
    headers[j] <- files[i]
    j <- j + 1
  }
}

lists[[1]][[12]] <- str_sub(lists[[1]][[11]], -4, -1)
lists[[1]][[11]] <- str_sub(lists[[1]][[11]], 1, 5)
lists[[3]][[12]] <- ""
lists[[5]] <- c("Peter", "Piper", "picked", "a", "peck", "of", "pickled", "peppers", "Peggy", "Babcock", "Peggy", "Babcock")
headers[[5]] <- "Key"

data_matrix <- do.call(cbind, lists)
colnames(data_matrix) <- headers

hd = NULL
for(i in 1:ncol(data_matrix)){
  hd[i] <- hamming.distance(data_matrix[,i], data_matrix[,5])
}

data_matrix <- rbind(data_matrix, hd)
rownames(data_matrix)[nrow(data_matrix)] <- "hamming distance"

file_out <- paste(getwd(), "collected/Watson_collected.csv", sep = "/")
write.csv(data_matrix, file = file_out, na = "")