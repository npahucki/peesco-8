//
//  Drink+Helper.m
//  BartendroPad
//
//  Created by Pablo Castro on 12/11/13.
//  Copyright (c) 2013 witty. All rights reserved.
//

#import "Drink+Helper.h"

@implementation Drink (Helper)

- (void) fillWithAttributes:(NSDictionary *)attributes{

    /*
     @property (nonatomic, retain) NSNumber * drink_id;
     @property (nonatomic, retain) NSString * desc;
     @property (nonatomic, retain) NSNumber * name_id;
     @property (nonatomic, retain) NSNumber * sugg_size;
     @property (nonatomic, retain) NSNumber * popular;
     @property (nonatomic, retain) NSNumber * available;
     */
    
    
    //NSLog(@"attr: %@", attributes);
    
    self.drink_id  = @([[attributes valueForKeyPath:@"id"]        intValue]);
    self.desc      =    [attributes valueForKeyPath:@"desc"];
    self.name_id   = @([[attributes valueForKeyPath:@"name_id"]   intValue]);
    self.sugg_size = @([[attributes valueForKeyPath:@"sugg_size"] intValue]);
    self.popular   = @([[attributes valueForKeyPath:@"popular"]   intValue]);
    self.available = @([[attributes valueForKeyPath:@"available"] intValue]);
    
}

@end
