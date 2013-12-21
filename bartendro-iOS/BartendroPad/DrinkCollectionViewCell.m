//
//  DrinkCollectionViewCell.m
//  BartendroPad
//
//  Created by Pablo Castro on 12/11/13.
//  Copyright (c) 2013 witty. All rights reserved.
//

#import "DrinkCollectionViewCell.h"

@implementation DrinkCollectionViewCell

@synthesize drink;


- (id)initWithFrame:(CGRect)frame
{
    self = [super initWithFrame:frame];
    if (self) {
        // Initialization code
    }
    return self;
}

/*
// Only override drawRect: if you perform custom drawing.
// An empty implementation adversely affects performance during animation.
- (void)drawRect:(CGRect)rect
{
    // Drawing code
}
*/

-(void)populateUIwithDatafrom:(Drink *)aDrink{

    self.backgroundColor = [UIColor whiteColor];
    self.drinkDescription.text = aDrink.desc;
    self.drinkName.text = aDrink.name;
    
    [self setDrink:aDrink];

}


- (IBAction)pourDrink:(id)sender {
    
    NSLog(@"Pouring a drink called: %@", self.drink.name);
    NSLog(@"With the ID: %@", self.drink.drink_id);
    
    [self getDrinkDescription:self.drink.drink_id.intValue];
    
}


-(void) getDrinkDescription:(int)drinkID{
    
    NSLog(@"Getting drink with ID: %d", drinkID);
    
    AFHTTPRequestOperationManager * manager = [AFHTTPRequestOperationManager manager];
    
    NSString * wsCall = [[NSString alloc] initWithFormat:@"http://localhost:8080/ws/drink_info/%d", drinkID ];
    
    [manager GET:wsCall
      parameters:nil
     
         success:^(AFHTTPRequestOperation *operation, id responseObject) {
             NSLog(@"JSON: %@", responseObject);
         }
     
         failure:^(AFHTTPRequestOperation *operation, NSError *error) {
             NSLog(@"Error: %@", error);
         }
     ];
}





@end
